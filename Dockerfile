# Use Python slim image
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies needed for OpenCV headless
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install PyTorch CPU-only first (much smaller)
RUN pip install --no-cache-dir \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    torch==2.9.1+cpu \
    torchvision==0.24.1+cpu

# Install other dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run with gunicorn (use shell form to expand $PORT)
CMD gunicorn api:app --bind 0.0.0.0:${PORT:-5000} --workers 2 --timeout 120

