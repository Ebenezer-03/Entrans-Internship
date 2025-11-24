# Multi-stage Dockerfile for NLP/NLU 3-Day Project
# Supports both CPU and GPU execution

FROM python:3.10-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Download spaCy models
RUN python -m spacy download en_core_web_sm

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p data/samples data/downloads examples/outputs logs

# Set Python path
ENV PYTHONPATH=/app:$PYTHONPATH

# Default command runs smoke test
CMD ["python", "tests/test_smoke_model.py"]

# For interactive use:
# docker run -it --rm nlp-nlu-3day bash

# For GPU support, use:
# docker run --gpus all -it --rm nlp-nlu-3day
