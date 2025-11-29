# 🚂 Railway Backend Deployment Guide

This guide will help you deploy your Flask backend to Railway, then connect it to your Netlify frontend.

## Step 1: Deploy Backend to Railway

### Option A: Using Railway Web Interface (Recommended - Easiest)

1. **Go to Railway**: Visit [railway.app](https://railway.app)
   - Sign up/login (GitHub login works great!)

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Authorize Railway to access your GitHub
   - Select your repository: `nico-mannarelli/bird-camera`

3. **Railway Auto-Detection**:
   - Railway will automatically detect your `Procfile`
   - It will start deploying immediately
   - Watch the deployment logs

4. **Wait for Deployment** (5-10 minutes first time):
   - Installing Python dependencies
   - Downloading model on first request
   - Building the application

5. **Get Your Backend URL**:
   - Once deployed, click on your service
   - Go to "Settings" tab
   - Scroll to "Domains" section
   - Railway provides a URL like: `https://your-app-name.up.railway.app`
   - **COPY THIS URL** - you'll need it in Step 2!

### Option B: Using Railway CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

## Step 2: Update Frontend with Backend URL

1. **Open `script.js`** in your editor

2. **Find line 7** (the production API_URL):
   ```javascript
   : 'https://your-backend-url.railway.app';  // TODO: Replace...
   ```

3. **Replace with your actual Railway URL**:
   ```javascript
   : 'https://your-actual-app-name.up.railway.app';
   ```

4. **Save the file**

5. **Commit and push**:
   ```bash
   git add script.js
   git commit -m "Update backend URL to Railway"
   git push origin main
   ```

## Step 3: Test Your Setup

1. **Test Backend** (optional):
   - Visit: `https://your-app.up.railway.app/health`
   - Should return: `{"status":"healthy"}`

2. **Test Frontend**:
   - Visit your Netlify site
   - Upload a bird image
   - Should work! 🎉

## Step 4: Configure Railway (Optional)

### Set Environment Variables (if needed):
- Go to your Railway service → "Variables" tab
- Add any environment variables your app needs

### Increase Resources (if needed):
- Railway free tier: 512MB RAM, $5/month credit
- If you need more, upgrade in "Settings" → "Usage"

## 🎯 What You Get

✅ **No timeout limits** - Railway doesn't have function timeouts  
✅ **Persistent containers** - Model stays loaded between requests  
✅ **Fast responses** - After first load, responses are quick  
✅ **Easy scaling** - Can upgrade resources if needed  
✅ **Free tier** - $5/month credit (usually enough for small apps)  

## 🐛 Troubleshooting

### Backend not responding?
- Check Railway logs: Service → "Deployments" → Click latest → View logs
- Make sure `Procfile` exists and is correct
- Verify `requirements.txt` has all dependencies

### CORS errors?
- Backend already has `flask-cors` configured
- Check that backend URL in `script.js` is correct
- Make sure backend is actually running

### Model download fails?
- Check Railway logs for download errors
- Verify Google Drive file ID in `api.py` is correct
- Ensure file is publicly accessible

### First request very slow?
- Normal! Model downloads (~23MB) and loads on first request
- Takes 30-60 seconds first time
- Subsequent requests are fast (~1-2 seconds)

## 📊 Monitoring

- **View logs**: Railway dashboard → Your service → "Deployments" → Logs
- **Monitor usage**: Settings → Usage (see RAM, CPU, bandwidth)
- **Check health**: Visit `/health` endpoint

## 💰 Cost

- **Free tier**: $5/month credit
- **Typical usage**: ~$2-4/month for small apps
- **Upgrade**: If you exceed free tier, pay-as-you-go

## 🎉 You're Done!

Your app is now:
- ✅ Frontend on Netlify (fast CDN)
- ✅ Backend on Railway (no timeouts, reliable)
- ✅ Fully functional bird detection!

