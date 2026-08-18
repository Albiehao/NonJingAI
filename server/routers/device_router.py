from __future__ import annotations

import os

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.utils.auth_middleware import get_db, get_required_user
from src.storage.postgres.models_business import User
from src.storage.postgres.models_mqtt import MqttDeviceBinding

router = APIRouter(prefix="/devices", tags=["MQTT设备"])

MQTT_GATEWAY_URL = os.getenv("MQTT_GATEWAY_URL", "http://mqtt-gateway:8090").rstrip("/")
MQTT_GATEWAY_API_KEY = os.getenv("MQTT_GATEWAY_API_KEY", "change-me")
GATEWAY_TIMEOUT = 5.0


class BindDeviceRequest(BaseModel):
    sn: str = Field(min_length=1, max_length=128)
    password: str = Field(min_length=1, max_length=256)


async def _verify_gateway_credential(sn: str, password: str) -> bool:
    try:
        async with httpx.AsyncClient(timeout=GATEWAY_TIMEOUT) as client:
            response = await client.post(
                f"{MQTT_GATEWAY_URL}/api/v1/devices/verify",
                headers={"X-API-Key": MQTT_GATEWAY_API_KEY},
                json={"sn": sn, "password": password},
            )
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="MQTT设备认证服务暂时不可用",
        ) from exc

    if response.status_code == 401:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="MQTT设备认证服务配置错误",
        )

    if response.status_code >= 500:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="MQTT设备认证服务暂时不可用",
        )

    if response.status_code != 200:
        return False

    data = response.json()
    return bool(data.get("valid"))


@router.get("")
async def list_devices(
    current_user: User = Depends(get_required_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(MqttDeviceBinding)
        .where(MqttDeviceBinding.user_id == current_user.id)
        .order_by(MqttDeviceBinding.created_at.desc())
    )
    return [item.to_dict() for item in result.scalars().all()]


@router.post("/bind")
async def bind_device(
    body: BindDeviceRequest,
    current_user: User = Depends(get_required_user),
    db: AsyncSession = Depends(get_db),
):
    sn = body.sn.strip()
    if not sn:
        raise HTTPException(status_code=400, detail="SN不能为空")

    existing_result = await db.execute(
        select(MqttDeviceBinding).where(MqttDeviceBinding.sn == sn)
    )
    existing = existing_result.scalar_one_or_none()

    if existing:
        if existing.user_id == current_user.id:
            return {
                "message": "设备已绑定",
                "device": existing.to_dict(),
            }
        raise HTTPException(status_code=409, detail="该设备已被其他用户绑定")

    if not await _verify_gateway_credential(sn, body.password):
        raise HTTPException(status_code=400, detail="SN或设备密码错误")

    binding = MqttDeviceBinding(user_id=current_user.id, sn=sn)
    db.add(binding)
    await db.commit()
    await db.refresh(binding)

    return {
        "message": "绑定成功",
        "device": binding.to_dict(),
    }


@router.delete("/{sn}")
async def unbind_device(
    sn: str,
    current_user: User = Depends(get_required_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(MqttDeviceBinding).where(
            MqttDeviceBinding.sn == sn,
            MqttDeviceBinding.user_id == current_user.id,
        )
    )
    binding = result.scalar_one_or_none()

    if not binding:
        raise HTTPException(status_code=404, detail="设备不存在或未绑定")

    await db.delete(binding)
    await db.commit()
    return {"message": "解绑成功", "sn": sn}
