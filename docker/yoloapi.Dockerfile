FROM python:3.10-slim

COPY --from=ghcr.io/astral-sh/uv:0.7.2 /uv /uvx /bin/

WORKDIR /app

ENV TZ=Asia/Shanghai \
    UV_SYSTEM_PYTHON=1 \
    UV_COMPILE_BYTECODE=1

RUN sed -i 's|deb.debian.org|mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list.d/debian.sources \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ✅ 先装 CPU torch
RUN uv pip install torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/cpu

COPY yoloapi/pyproject.toml .

# ✅ 关键：禁止覆盖 torch
RUN uv sync --no-dev \
    --index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    --no-install-package torch \
    --no-install-package torchvision \
    --no-install-package torchaudio

COPY yoloapi/ .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]