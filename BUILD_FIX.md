# 🔧 Railway Build Timeout Fix

## Problem
Railway build is timing out because PyTorch is very large (~2GB with CUDA).

## Solution Applied
1. **CPU-only PyTorch** - Using CPU version is ~200MB instead of ~2GB
2. **Optimized requirements.txt** - Added PyTorch CPU index
3. **Railway config** - Added `railway.json` for better build settings

## If Build Still Times Out

### Option 1: Upgrade Railway Plan (Recommended)
- Free tier: 5-minute build timeout
- Pro tier: Longer timeout limits
- Go to Railway → Settings → Upgrade

### Option 2: Use Pre-built Docker Image
Create a `Dockerfile` instead:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Run
CMD ["gunicorn", "api:app", "--bind", "0.0.0.0:$PORT"]
```

### Option 3: Split Dependencies
Install PyTorch separately in a build script to cache it better.

## Current Status
✅ Updated to use CPU-only PyTorch (much faster)
✅ Added railway.json configuration
✅ Committed and pushed

**Next**: Railway should automatically rebuild. If it still times out, try the Dockerfile approach above.

