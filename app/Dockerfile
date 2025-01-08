# Stage 1: Requirements
FROM python:3.9-slim as requirements-stage

WORKDIR /tmp

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry==1.7.1 && \
    poetry config virtualenvs.create false

# Copy dependency files
COPY ./pyproject.toml ./poetry.lock* /tmp/

# Install dependencies and export requirements
RUN poetry config installer.max-workers 10 && \
    poetry install --no-interaction --no-root && \
    poetry export --format requirements.txt --output requirements.txt --without-hashes

# Stage 2: Final image
FROM python:3.9-slim

WORKDIR /app

# Build initial setup
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgl1-mesa-glx \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install system package
COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./models /app/models
COPY . /app

# Container status checker : Job scheduler
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]