# Use slim variant for smaller base image
FROM python:3.12.3-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000 \
    # Prevents Python from writing .pyc files
    PYTHONUNBUFFERED=1 \
    # Prevents pip from caching downloaded packages
    PIP_NO_CACHE_DIR=1 \
    # Disables the pip version check
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libgl1-mesa-glx \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/* && \
    # Create non-root user for security
    adduser --disabled-password --gecos "" appuser

# Copy only the necessary files first
COPY ./models ./models
COPY ./main.py ./api.py ./config.py ./database.py ./dependencies.py ./

# Install Python packages
# Organized by functionality for better maintainability
RUN pip install --no-cache-dir \
    # Web framework and related
    "fastapi>=0.105.0" \
    "uvicorn[standard]>=0.34.0" \
    "python-multipart>=0.0.7" \
    # Database
    "sqlalchemy>=2.0.36" \
    # HTTP client
    "requests>=2.32.3" \
    # ML/DL related
    "ultralytics[cpu]>=8.3.54" \
    "numpy>=1.26.4" \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    "torch>=2.0.0" \
    # Utilities
    "python-dotenv>=1.0.0" && \
    # Change ownership of the app directory
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]