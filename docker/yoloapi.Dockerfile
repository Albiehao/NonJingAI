FROM python:3.10-slim


WORKDIR /app

ENV TZ=Asia/Shanghai \
    UV_COMPILE_BYTECODE=1

RUN sed -i 's|deb.debian.org|mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list.d/debian.sources \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        libglib2.0-0t64 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv==0.7.2 \
    --index-url https://pypi.tuna.tsinghua.edu.cn/simple

COPY yolo/pyproject.toml .

# 创建虚拟环境，先装 CPU 版 torch，再装其余依赖
RUN uv venv && \
    uv pip install torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/cpu

RUN UV_HTTP_TIMEOUT=120 uv pip install . \
    --index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 用 headless 版替换 ultralytics 带入的 opencv-python（省 libgl1/Mesa 依赖）
RUN uv pip install opencv-python-headless --force-reinstall \
    --index-url https://pypi.tuna.tsinghua.edu.cn/simple

COPY yolo/ .

EXPOSE 8000

CMD ["/app/.venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
