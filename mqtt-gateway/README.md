# MQTT Gateway

当前阶段只实现设备身份、MQTT CONNECT 鉴权和用户设备绑定基础，不处理业务 Payload。

## 身份约定

每台设备固定使用：

- `SN = MQTT Username`
- `SN = MQTT ClientId`
- `Device Password = MQTT Password`

例如：

```text
SN: QX2026000001
Username: QX2026000001
ClientId: QX2026000001
Password: device-secret
```

## 组件

```text
Device
  │ MQTT CONNECT :1883
  ▼
EMQX
  │ HTTP authentication
  ▼
mqtt-gateway :8090
  │
  └─ SQLite credential store
```

`mqtt-gateway` 只负责设备凭据和 EMQX 鉴权。NonJingAI 主系统保存用户与 SN 的绑定关系，不保存 MQTT 明文密码。

## 启动

仓库根目录执行：

```bash
docker compose up -d --build mqtt-gateway emqx api web
```

根目录的 `docker-compose.override.yml` 会自动把 MQTT 服务合并进现有开发环境。

端口：

- MQTT TCP: `1883`
- EMQX Dashboard: `18083`
- MQTT Gateway HTTP API: `8090`

## 注册测试设备凭据

设备凭据应在生产/烧录阶段注册。开发环境可使用：

```bash
curl -X POST http://localhost:8090/api/v1/devices/bind \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: change-me' \
  -d '{"sn":"QX2026000001","password":"device-secret"}'
```

生产环境必须修改 `MQTT_GATEWAY_API_KEY`。

## MQTT CONNECT

设备连接参数：

```text
Host: <server-ip>
Port: 1883
ClientId: QX2026000001
Username: QX2026000001
Password: device-secret
```

只有以下条件全部满足才允许建立 MQTT Session：

1. Username 非空；
2. ClientId 非空；
3. `Username == ClientId`；
4. SN 格式合法；
5. SN 已注册；
6. 密码正确。

## Topic ACL

认证成功后，设备只允许：

```text
PUBLISH   devices/{sn}/up
PUBLISH   devices/{sn}/status
PUBLISH   devices/{sn}/ack
SUBSCRIBE devices/{sn}/down
```

其他 Topic 默认拒绝。

目前这些 Topic 只建立通信边界，Gateway 暂不解析里面的温湿度、控制指令或其他业务数据。
