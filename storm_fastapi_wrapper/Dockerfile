# Development Dockerfile for STORM + FastAPI
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry

# Clone STORM repo and install in editable mode
RUN git clone https://github.com/stanford-oval/storm.git /app/storm && \
    cd /app/storm && \
    pip install -e .

# Clone your FastAPI wrapper
RUN git clone https://github.com/ManavRajput/storm_wraped_Fastapi.git /app/storm_fastapi_wrapper

# Install your project dependencies
WORKDIR /app/storm_fastapi_wrapper
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Install additional requirements
RUN pip install --no-cache-dir \
    google-generativeai>=0.3.0 \
    python-dotenv \
    uvicorn

# Environment setup
ARG GEMINI_API_KEY="dummy_key_for_dev"
ENV GEMINI_API_KEY=$GEMINI_API_KEY \
    GEMINI_MODEL="gemini-1.0-pro" \
    PYTHONPATH="/app:/app/storm:/app/storm_fastapi_wrapper" \
    GOOGLE_API_REGION="us-central1"

# Expose port
EXPOSE 8000

# Run your FastAPI app with auto-reload
WORKDIR /app/storm_fastapi_wrapper
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
