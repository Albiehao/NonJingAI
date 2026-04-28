FROM python:3.10-slim


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

RUN pip install --no-cache-dir uv==0.7.2 \
    --index-url https://pypi.tuna.tsinghua.edu.cn/simple

COPY yolo/pyproject.toml .

RUN uv sync --no-dev --no-install-project \
    --index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN uv pip install --python /app/.venv/bin/python torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/cpu

COPY yolo/ .

EXPOSE 8000

CMD ["/app/.venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
