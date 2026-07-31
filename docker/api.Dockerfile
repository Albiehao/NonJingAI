# syntax=docker/dockerfile:1

# 使用轻量级 Python 基础镜像
FROM python:3.12-slim

# 安装固定版本的 uv
COPY --from=ghcr.io/astral-sh/uv:0.7.2 /uv /uvx /bin/

# 从 Node 20 镜像复制 Node.js、npm 及相关文件
COPY --from=node:20-slim /usr/local/bin /usr/local/bin
COPY --from=node:20-slim /usr/local/lib/node_modules /usr/local/lib/node_modules
COPY --from=node:20-slim /usr/local/include /usr/local/include
COPY --from=node:20-slim /usr/local/share /usr/local/share

# 设置工作目录
WORKDIR /app

# 环境变量
ENV TZ=Asia/Shanghai \
    UV_PROJECT_ENVIRONMENT=/usr/local \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive

# Node 20 已自带兼容版本的 npm，不安装 npm@latest
RUN set -eux; \
    node --version; \
    npm --version; \
    npm cache clean --force

# 设置时区、替换 Debian 软件源并安装系统依赖
RUN set -eux; \
    ln -snf "/usr/share/zoneinfo/${TZ}" /etc/localtime; \
    echo "${TZ}" > /etc/timezone; \
    sed -i \
        's|deb.debian.org|mirrors.tuna.tsinghua.edu.cn|g' \
        /etc/apt/sources.list.d/debian.sources; \
    sed -i \
        's|security.debian.org/debian-security|mirrors.tuna.tsinghua.edu.cn/debian-security|g' \
        /etc/apt/sources.list.d/debian.sources; \
    apt-get update; \
    apt-get install -y --no-install-recommends --fix-missing \
        curl \
        ffmpeg \
        libsm6 \
        libxext6 \
        fonts-noto-cjk \
        fontconfig; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/*

# 先复制 Python 项目配置，以便充分利用 Docker 构建缓存
COPY ../pyproject.toml /app/pyproject.toml
COPY ../.python-version /app/.python-version
COPY ../uv.lock /app/uv.lock

# 安装生产环境 Python 依赖
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev --frozen

# 复制项目代码
COPY ../src /app/src
COPY ../server /app/server