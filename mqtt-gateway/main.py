"""Standalone MQTT credential gateway."""
from __future__ import annotations

import base64
import hashlib
import hmac
import os
import re
import secrets
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path

from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field

API_KEY = os.getenv("MQTT_GATEWAY_API_KEY", "change-me")
EMQX_AUTH_SHARED_SECRET = os.getenv("EMQX_AUTH_SHARED_SECRET", "emqx-internal")
DB_PATH = Path(os.getenv("MQTT_GATEWAY_DB", "/data/mqtt-gateway.db"))
ITERATIONS = 210000
SN_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")

app = FastAPI(title="Qianxun MQTT Gateway", version="0.3.0")

class DeviceCredential(BaseModel):
    sn: str = Field(min_length=1, max_length=128)
    password: str = Field(min_length=1, max_length=256)

class EmqxAuthRequest(BaseModel):
    username: str | None = None
    password: str | None = None
    clientid: str | None = None


def db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c


def init_db():
    with closing(db()) as c:
        c.execute("""CREATE TABLE IF NOT EXISTS mqtt_device_credentials(
        sn TEXT PRIMARY KEY,salt TEXT NOT NULL,password_hash TEXT NOT NULL,created_at TEXT NOT NULL)""")
        c.commit()


def valid_sn(sn):
    return bool(SN_PATTERN.fullmatch(sn))


def encode(v):
    return base64.urlsafe_b64encode(v).decode()


def decode(v):
    return base64.urlsafe_b64decode(v.encode())


def hash_pwd(p,s):
    return hashlib.pbkdf2_hmac("sha256",p.encode(),s,ITERATIONS)


def verify(sn,password):
    if not valid_sn(sn):
        return False
    with closing(db()) as c:
        row=c.execute("select salt,password_hash from mqtt_device_credentials where sn=?",(sn,)).fetchone()
    return bool(row and hmac.compare_digest(hash_pwd(password,decode(row['salt'])),decode(row['password_hash'])))


def api_key(x_api_key: str | None = Header(default=None)):
    if not x_api_key or not hmac.compare_digest(x_api_key,API_KEY):
        raise HTTPException(status_code=401,detail="invalid api key")


def emqx_secret(x_emqx_auth: str | None = Header(default=None)):
    if not x_emqx_auth or not hmac.compare_digest(x_emqx_auth,EMQX_AUTH_SHARED_SECRET):
        raise HTTPException(status_code=401,detail="invalid emqx secret")

@app.on_event("startup")
def startup():
    init_db()

@app.post("/api/v1/devices/provision",dependencies=[Depends(api_key)])
def provision(body: DeviceCredential):
    sn=body.sn.strip()
    if not valid_sn(sn):
        raise HTTPException(400,"invalid sn")
    salt=secrets.token_bytes(16)
    with closing(db()) as c:
        c.execute("insert or replace into mqtt_device_credentials values(?,?,?,?)",(sn,encode(salt),encode(hash_pwd(body.password,salt)),datetime.now(timezone.utc).isoformat()))
        c.commit()
    return {"sn":sn,"provisioned":True}

@app.post("/api/v1/devices/verify",dependencies=[Depends(api_key)])
def device_verify(body: DeviceCredential):
    return {"sn":body.sn,"valid":verify(body.sn.strip(),body.password)}

@app.post("/emqx/auth",dependencies=[Depends(emqx_secret)])
def emqx_auth(body: EmqxAuthRequest):
    if not body.username or body.username!=body.clientid or not verify(body.username,body.password or ""):
        return {"result":"deny"}
    return {"result":"allow","acl":[{"permission":"allow","action":"publish","topic":"devices/${clientid}/up"},{"permission":"allow","action":"publish","topic":"devices/${clientid}/status"},{"permission":"allow","action":"subscribe","topic":"devices/${clientid}/down"}]}
