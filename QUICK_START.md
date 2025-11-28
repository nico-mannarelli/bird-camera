# Quick Start Guide - Netlify Deployment

## 🚀 Quick Deployment Steps

### 1. Deploy Backend (Choose one platform)

#### Option A: Railway (Easiest)
1. Go to [railway.app](https://railway.app) and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect the `Procfile` and deploy
5. Copy your deployment URL (e.g., `https://your-app.railway.app`)

#### Option B: Render
1. Go to [render.com](https://render.com) and sign up
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn api:app --bind 0.0.0.0:$PORT`
5. Deploy and copy your URL

### 2. Update Frontend API URL

Edit `script.js` and replace the backend URL:
```javascript
const API_URL = 'https://your-actual-backend-url.railway.app';
```

### 3. Deploy Frontend to Netlify

1. Go to [netlify.com](https://app.netlify.com) and sign up
2. Click "Add new site" → "Import an existing project"
3. Connect your GitHub repository
4. Build settings:
   - **Base directory**: (leave empty)
   - **Build command**: (leave empty)
   - **Publish directory**: `.` (current directory)
5. Click "Deploy site"
6. Your site will be live at `https://your-site.netlify.app`

### 4. Test Your Deployment

1. Visit your Netlify URL
2. Upload a bird image
3. Check that detections work!

## 📝 Notes

- First backend request may take 30-60 seconds (model download + load)
- Backend needs at least 1GB RAM
- Model file (~23MB) downloads automatically on first run

## 🐛 Troubleshooting

**CORS errors?**
- Make sure your backend URL in `script.js` is correct
- Check that `flask-cors` is installed in requirements.txt

**Model not loading?**
- Check backend logs for download errors
- Verify Google Drive file ID in `api.py` is correct

**Timeout errors?**
- Increase timeout on your hosting platform
- First request is always slower (model loading)

