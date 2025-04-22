FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (needed for some Python packages)
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy project files
COPY pyproject.toml poetry.lock ./
COPY storm_fastapi_wrapper ./storm_fastapi_wrapper
COPY utils ./utils

# Clone the STORM repo
RUN git clone https://github.com/stanford-oval/storm.git && \
    echo "Cloned STORM repo"

# Install dependencies with Poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

# Install Google Generative AI package (for Gemini)
RUN pip install --no-cache-dir \
    google-generativeai>=0.3.0 \
    python-dotenv

# Create a directory for API keys
RUN mkdir -p /app/config && chmod 700 /app/config

# Environment variables for Gemini
ENV GEMINI_API_KEY="your-api-key-here" \
    GEMINI_MODEL="gemini-2.0-flash-lite-001" \
    GOOGLE_API_REGION="us-central1"

# Expose the FastAPI app port
EXPOSE 8000

# Default command to run the app
CMD ["uvicorn", "storm_fastapi_wrapper.main:app", "--host", "0.0.0.0", "--port", "8000"]