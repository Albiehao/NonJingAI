#!/bin/bash
# 生产环境部署脚本
# 在本地（Windows Git Bash）执行：构建镜像 → 传到服务器 → 部署
#
# 用法:
#   ./scripts/deploy-prod.sh                    # 构建+传输+部署
#   ./scripts/deploy-prod.sh --skip-build       # 只传输+部署
#   ./scripts/deploy-prod.sh --skip-transfer    # 只构建+部署（服务器已git pull）
#
# 前提:
#   - 本地安装 Docker
#   - 服务器 IP 47.114.88.3，密码 Zjh1980!

set -e

REMOTE_HOST="47.114.88.3"
REMOTE_USER="root"
REMOTE_PASS="Zjh1980!"
REMOTE_DIR="/var/www/qianxun"
COMPOSE_FILE="docker-compose.prod.yml"
IMAGE_TAR="/tmp/qianxun-images.tar"

# 要构建和传输的自定义镜像
IMAGES=(
  "qian-yuxi-api:0.5.prod"
  "qian-yuxi-web:0.5.prod"
  "qian-qianxun-server:0.0.1.prod"
  "qian-yolo-api:0.1.0"
)

# 要从镜像名提取的原始镜像名（docker save 用）
SAVE_IMAGES=(
  "qian-yuxi-api:0.5.prod"
  "qian-yuxi-web:0.5.prod"
  "qian-qianxun-server:0.0.1.prod"
  "qian-yolo-api:0.1.0"
)

# SSH 密码辅助（Windows Git Bash 用 SSH_ASKPASS）
setup_ssh_askpass() {
    export DISPLAY=:0
    export SSH_ASKPASS_REQUIRE=force
    export SSH_ASKPASS=/tmp/deploy-ssh-pass.sh
    cat > "$SSH_ASKPASS" << 'PASS'
#!/bin/sh
echo "Zjh1980!"
PASS
    chmod +x "$SSH_ASKPASS"
}

ssh_cmd() {
    ssh -o StrictHostKeyChecking=no -T "${REMOTE_USER}@${REMOTE_HOST}" "$@" < /dev/null
}

# 解析参数
SKIP_BUILD=false
SKIP_TRANSFER=false
for arg in "$@"; do
    case "$arg" in
        --skip-build) SKIP_BUILD=true ;;
        --skip-transfer) SKIP_TRANSFER=true ;;
    esac
done

echo "=========================================="
echo "  千寻 生产环境部署"
echo "=========================================="

# ---- 1. 构建 ----
if [ "$SKIP_BUILD" = false ]; then
    echo ""
    echo "[1/4] 构建 Docker 镜像..."

    docker compose -f docker-compose.prod.yml build api web yoloapi

    # 单独构建 qianxun-server（特殊 context）
    docker compose -f docker-compose.prod.yml build qianxun-server

    echo "      构建完成"
else
    echo "[1/4] 跳过构建"
fi

# ---- 2. 保存并压缩 ----
if [ "$SKIP_TRANSFER" = false ]; then
    echo ""
    echo "[2/4] 保存镜像到 $IMAGE_TAR ..."
    rm -f "$IMAGE_TAR"
    docker save -o "$IMAGE_TAR" "${SAVE_IMAGES[@]}"
    echo "      镜像大小: $(du -sh "$IMAGE_TAR" | cut -f1)"
else
    echo "[2/4] 跳过保存"
fi

# ---- 3. 传输 ----
if [ "$SKIP_TRANSFER" = false ]; then
    echo ""
    echo "[3/4] 传输镜像到服务器 ${REMOTE_HOST} ..."

    setup_ssh_askpass

    # 传输 tar 文件
    ssh_cmd "rm -f /root/qianxun-images.tar"
    SSH_ASKPASS="$SSH_ASKPASS" SSH_ASKPASS_REQUIRE=force \
        scp -o StrictHostKeyChecking=no "$IMAGE_TAR" "${REMOTE_USER}@${REMOTE_HOST}:/root/qianxun-images.tar"

    echo "      传输完成"
    rm -f "$IMAGE_TAR"
else
    echo "[3/4] 跳过传输"
fi

# ---- 4. 部署 ----
echo ""
echo "[4/4] 连接服务器部署..."

setup_ssh_askpass

ssh_cmd "
set -e
echo '      加载镜像...'
docker load -i /root/qianxun-images.tar 2>&1 | head -5
rm -f /root/qianxun-images.tar

echo '      进入项目目录...'
cd $REMOTE_DIR

echo '      检查 .env 配置...'
if ! grep -q '^STORAGE_PROXY_URL=' .env 2>/dev/null; then
    echo 'STORAGE_PROXY_URL=47.114.88.3' >> .env
fi

echo '      拉取外部镜像...'
docker compose -f $COMPOSE_FILE pull postgres neo4j milvus etcd minio 2>&1 | tail -3

echo '      启动所有服务...'
docker compose -f $COMPOSE_FILE up -d

echo '      等待健康检查...'
sleep 10
docker ps --format 'table {{.Names}}\t{{.Status}}' | grep -v 'milvus-etcd\|milvus-minio'
"

echo ""
echo "=========================================="
echo "  部署完成"
echo "=========================================="
