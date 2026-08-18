"""Standalone MQTT credential gateway.

This service owns MQTT device credentials and exposes:
- manufacturing/admin credential registration
- credential verification for the main business API
- EMQX HTTP authentication for MQTT CONNECT

It intentionally does not process telemetry or business payloads yet.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import os
import secrets
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path

from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field

APP_NAME = "Qianxun MQTT Gateway"
API_KEY = os.getenv("MQTT_GATEWAY_API_KEY", "change-me")
EMQX_AUTH_SHARED_SECRET = os.getenv("EMQX_AUTH_SHARED_SECRET", "emqx-internal")
DB_PATH = Path(os.getenv("MQTT_GATEWAY_DB", "/data/mqtt-gateway.db"))
PBKDF2_ITERATIONS = 210_000

app = FastAPI(title=APP_NAME, version="0.2.0")


class DeviceCredential(BaseModel):
    sn: str = Field(min_length=1, max_length=128)
    password: str = Field(min_length=1, max_length=256)


class VerifyResult(BaseModel):
    sn: str
    valid: bool


class EmqxAuthRequest(BaseModel):
    username: str | None = None
    password: str | None = None
    clientid: str | None = None


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _init_db() -> None:
    with closing(_connect()) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS mqtt_device_credentials (
                sn TEXT PRIMARY KEY,
                salt TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def _hash_password(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )


def _encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode("ascii")


def _decode(raw: str) -> bytes:
    return base64.urlsafe_b64decode(raw.encode("ascii"))


def _verify_password(password: str, salt: str, password_hash: str) -> bool:
    calculated = _hash_password(password, _decode(salt))
    return hmac.compare_digest(calculated, _decode(password_hash))


def _credential_valid(sn: str, password: str) -> bool:
    with closing(_connect()) as conn:
        row = conn.execute(
            "SELECT salt, password_hash FROM mqtt_device_credentials WHERE sn = ?",
            (sn,),
        ).fetchone()

    if not row:
        return False

    return _verify_password(password, row["salt"], row["password_hash"])


def _require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if not x_api_key or not hmac.compare_digest(x_api_key, API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid gateway api key",
        )


def _require_emqx_secret(x_emqx_auth: str | None = Header(default=None)) -> None:
    if not x_emqx_auth or not hmac.compare_digest(x_emqx_auth, EMQX_AUTH_SHARED_SECRET):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid EMQX authentication secret",
        )


@app.on_event("startup")
def startup() -> None:
    _init_db()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": APP_NAME}


@app.post("/api/v1/devices/bind", dependencies=[Depends(_require_api_key)])
def bind_device(body: DeviceCredential) -> dict:
    """Register a SN/password pair used by MQTT CONNECT authentication.

    This endpoint is intended for manufacturing/admin provisioning, not for the
    end-user binding page. Repeating the same SN/password is idempotent.
    """

    sn = body.sn.strip()
    if not sn:
        raise HTTPException(status_code=400, detail="SN cannot be empty")

    with closing(_connect()) as conn:
        row = conn.execute(
            "SELECT sn, salt, password_hash FROM mqtt_device_credentials WHERE sn = ?",
            (sn,),
        ).fetchone()

        if row:
            if not _verify_password(body.password, row["salt"], row["password_hash"]):
                raise HTTPException(status_code=409, detail="SN already exists with different credentials")
            return {"sn": sn, "bound": True, "created": False}

        salt = secrets.token_bytes(16)
        password_hash = _hash_password(body.password, salt)
        conn.execute(
            """
            INSERT INTO mqtt_device_credentials (sn, salt, password_hash, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                sn,
                _encode(salt),
                _encode(password_hash),
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        conn.commit()

    return {"sn": sn, "bound": True, "created": True}


@app.post(
    "/api/v1/devices/verify",
    response_model=VerifyResult,
    dependencies=[Depends(_require_api_key)],
)
def verify_device(body: DeviceCredential) -> VerifyResult:
    sn = body.sn.strip()
    return VerifyResult(sn=sn, valid=_credential_valid(sn, body.password))


@app.post("/emqx/auth", dependencies=[Depends(_require_emqx_secret)])
def emqx_authenticate(body: EmqxAuthRequest) -> dict:
    """Authenticate an MQTT CONNECT request from EMQX.

    Identity contract:
        Username == ClientId == device SN
        Password == device password

    The response also presets topic ACLs so one device cannot impersonate
    another device after authenticating.
    """

    username = (body.username or "").strip()
    clientid = (body.clientid or "").strip()
    password = body.password or ""

    # The project intentionally uses SN for both Username and ClientId.
    if not username or not clientid or username != clientid or not password:
        return {"result": "deny", "is_superuser": False}

    if not _credential_valid(username, password):
        return {"result": "deny", "is_superuser": False}

    return {
        "result": "allow",
        "is_superuser": False,
        "client_attrs": {
            "sn": username,
        },
        "acl": [
            {
                "permission": "allow",
                "action": "publish",
                "topic": "devices/${clientid}/up",
            },
            {
                "permission": "allow",
                "action": "publish",
                "topic": "devices/${clientid}/status",
            },
            {
                "permission": "allow",
                "action": "publish",
                "topic": "devices/${clientid}/ack",
            },
            {
                "permission": "allow",
                "action": "subscribe",
                "topic": "devices/${clientid}/down",
            },
        ],
    }
