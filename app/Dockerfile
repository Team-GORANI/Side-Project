FROM python:3.12-bookworm AS requirements-stage

WORKDIR /tmp

# Poetry 설치 및 설정
# Poetry 2.x: export 명령이 별도 플러그인으로 분리됨 (poetry.lock lock-version 2.1 요구)
RUN pip install --no-cache-dir poetry==2.4.1 poetry-plugin-export==1.10.0 && \
    poetry config virtualenvs.create false && \
    poetry config installer.max-workers 10

COPY ./pyproject.toml ./poetry.lock* /tmp/

# requirements.txt 생성
RUN pip install --no-cache-dir torch==2.13.0 && \
    python -m poetry install --no-interaction --no-root && \
    python -m poetry export --format requirements.txt --output requirements.txt --without-hashes

FROM python:3.12-slim-bookworm

WORKDIR /app

# Build initial setup
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgl1-mesa-glx \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install system package
COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt \
    --index-url https://pypi.org/simple \
    --extra-index-url https://download.pytorch.org/whl/cpu

COPY ./models /app/models
COPY . /app

# Container status checker : Job scheduler
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]