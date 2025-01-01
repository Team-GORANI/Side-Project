FROM python:3.9-slim as requirements-stage

WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

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
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt \
    --index-url https://pypi.org/simple \
    --extra-index-url https://download.pytorch.org/whl/cpu

RUN pip install ultralytics

# Copy model files first
COPY ./checkpoint /app/checkpoint
COPY ./models /app/models

# Then copy the rest of the application
COPY . /app

# Set environment variables
ENV PYTHONPATH=/app
ENV UVICORN_RELOAD=false

# Contatiner status checker : Job schedular
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]