from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.utils.auth_middleware import get_db, get_required_user
from src.storage.postgres.models_business import User
from src.storage.postgres.models_mqtt import MqttDeviceBinding

router = APIRouter(prefix="/devices", tags=["MQTT设备"])


class BindDeviceRequest(BaseModel):
    # 用户绑定关系只记录设备 SN，不负责 MQTT 认证
    sn: str = Field(min_length=1, max_length=128)


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

    existing = await db.scalar(
        select(MqttDeviceBinding).where(MqttDeviceBinding.sn == sn)
    )

    if existing:
        if existing.user_id == current_user.id:
            return {"message": "设备已绑定", "device": existing.to_dict()}
        raise HTTPException(status_code=409, detail="设备已被其他用户绑定")

    # 当前阶段只建立用户与设备 SN 的关系，不验证设备凭据
    binding = MqttDeviceBinding(
        user_id=current_user.id,
        sn=sn,
    )

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
    binding = await db.scalar(
        select(MqttDeviceBinding).where(
            MqttDeviceBinding.sn == sn,
            MqttDeviceBinding.user_id == current_user.id,
        )
    )

    if not binding:
        raise HTTPException(status_code=404, detail="设备不存在或未绑定")

    await db.delete(binding)
    await db.commit()

    return {"message": "解绑成功", "sn": sn}
