#!/bin/bash
#
# 千寻生产环境开机自启脚本
# 配合 systemd 服务 qianxun-prod.service 使用
#
# 安装:
#   cp scripts/qianxun-prod.service /etc/systemd/system/
#   systemctl daemon-reload && systemctl enable qianxun-prod

# 强制使用原生 Docker，防止被 DOCKER_HOST 环境变量误导
export DOCKER_HOST=unix:///var/run/docker.sock

PROJECT_DIR="/var/www/qianxun"
COMPOSE_FILE="docker-compose.prod.yml"

# 清理残留的 docker-proxy 僵尸进程，避免端口冲突
killall -9 docker-proxy 2>/dev/null || true

# 启动 frpc 内网穿透
if systemctl is-enabled frpc.service >/dev/null 2>&1; then
    systemctl start frpc.service 2>/dev/null || true
fi

# 关闭防火墙
ufw disable 2>/dev/null || true

# 等待 Docker 守护进程就绪
echo "等待 Docker 守护进程..."
until docker info >/dev/null 2>&1; do
    sleep 2
done

cd "$PROJECT_DIR"

# 确保必需的环境变量
touch .env
if ! grep -q "^STORAGE_PROXY_URL=" .env 2>/dev/null; then
    echo "STORAGE_PROXY_URL=47.114.88.3" >> .env
fi

echo "启动千寻生产服务..."
until docker compose -f "$COMPOSE_FILE" up -d; do
    echo "[$(date)] 启动失败，10 秒后重试..."
    killall -9 docker-proxy 2>/dev/null || true
    sleep 10
done

echo "千寻生产服务启动完成"
docker compose -f "$COMPOSE_FILE" ps
