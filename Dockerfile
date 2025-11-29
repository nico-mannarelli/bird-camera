# Use Python slim image for smaller size
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies needed for OpenCV and PyTorch
# Note: Using opencv-python-headless, so minimal dependencies needed
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install PyTorch CPU-only first (much smaller, ~200MB vs ~2GB)
RUN pip install --no-cache-dir \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    torch==2.0.1 \
    torchvision==0.15.2

# Install other dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE $PORT

# Run with gunicorn
CMD gunicorn api:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120

