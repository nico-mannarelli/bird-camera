# Deployment Guide

This guide explains how to deploy the Bird Species Detector to Netlify (frontend) and a backend service.

## Architecture

- **Frontend**: Static HTML/CSS/JS hosted on Netlify
- **Backend**: Flask API deployed on Railway, Render, or Fly.io (due to ML model size)

## Option 1: Deploy Backend on Railway (Recommended)

### Backend Deployment (Railway)

1. **Install Railway CLI** (optional, or use web interface):
   ```bash
   npm i -g @railway/cli
   railway login
   ```

2. **Deploy to Railway**:
   ```bash
   railway init
   railway up
   ```

3. **Set Environment Variables** (if needed):
   - Railway will automatically detect the `Procfile` and deploy

4. **Get your backend URL**:
   - Railway will provide a URL like: `https://your-app.railway.app`
   - Copy this URL

### Frontend Deployment (Netlify)

1. **Update API URL** in `static/script.js`:
   ```javascript
   const API_URL = 'https://your-app.railway.app';
   ```

2. **Deploy to Netlify**:
   - Go to [Netlify](https://app.netlify.com)
   - Click "Add new site" → "Import an existing project"
   - Connect your GitHub repository
   - Set build settings:
     - **Base directory**: (leave empty)
     - **Build command**: (leave empty or `echo "No build needed"`)
     - **Publish directory**: `static`
   - Click "Deploy site"

3. **Configure redirects** (already in `netlify.toml`):
   - Netlify will automatically use the `netlify.toml` file

## Option 2: Deploy Backend on Render

### Backend Deployment (Render)

1. **Create a new Web Service** on [Render](https://render.com)

2. **Connect your repository**

3. **Configure**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn api:app --bind 0.0.0.0:$PORT`
   - **Environment**: Python 3

4. **Deploy** and get your backend URL

### Frontend Deployment (Netlify)

Same as Option 1, but use your Render backend URL.

## Option 3: Deploy Backend on Fly.io

### Backend Deployment (Fly.io)

1. **Install Fly CLI**:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Create `fly.toml`** (if not exists):
   ```bash
   fly launch
   ```

3. **Deploy**:
   ```bash
   fly deploy
   ```

## Local Development

1. **Start the backend**:
   ```bash
   python api.py
   ```
   Backend will run on `http://localhost:5000`

2. **Serve the frontend**:
   ```bash
   cd static
   python -m http.server 8000
   ```
   Or use any static file server

3. **Update `static/script.js`**:
   ```javascript
   const API_URL = 'http://localhost:5000';
   ```

## Important Notes

- The model file (`best.pt`) will be downloaded automatically on first run
- Backend needs at least 1GB RAM for PyTorch and YOLOv8
- First request may be slow as the model loads
- Consider using model caching or a warm-up endpoint

## Troubleshooting

### CORS Errors
- Make sure `flask-cors` is installed
- Check that the backend URL in `script.js` is correct

### Model Download Issues
- Ensure the Google Drive file ID is correct in `api.py`
- Check that `gdown` is installed

### Timeout Issues
- Increase timeout on your hosting platform
- Consider optimizing the model or using a lighter version

