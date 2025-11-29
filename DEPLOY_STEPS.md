# Step-by-Step Deployment Guide

Follow these steps to deploy your Bird Detection app.

## Step 1: Deploy Backend to Railway 🚂

### Option A: Using Railway Web Interface (Recommended)

1. **Go to Railway**: Visit [railway.app](https://railway.app) and sign up/login
2. **Create New Project**: 
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Authorize Railway to access your GitHub
   - Select your repository: `nico-mannarelli/bird-camera`
3. **Railway Auto-Detection**:
   - Railway will automatically detect your `Procfile`
   - It will start deploying
4. **Wait for Deployment**:
   - First deployment takes 5-10 minutes (installing dependencies)
   - Watch the logs for progress
5. **Get Your Backend URL**:
   - Once deployed, click on your service
   - Go to "Settings" → "Domains"
   - Railway provides a URL like: `https://your-app-name.up.railway.app`
   - **COPY THIS URL** - you'll need it for the frontend!

### Option B: Using Railway CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize and deploy
railway init
railway up
```

## Step 2: Update Frontend with Backend URL 🔗

Once you have your Railway backend URL, update `script.js`:

1. Open `script.js` in your editor
2. Find line 10 (the production API_URL)
3. Replace `'https://your-backend-url.railway.app'` with your actual Railway URL
4. Save the file

Example:
```javascript
const API_URL = isLocalhost 
    ? 'http://localhost:5000'  // Local development
    : 'https://bird-camera-production.up.railway.app';  // Your actual URL
```

## Step 3: Commit and Push Changes 📤

```bash
git add script.js
git commit -m "Update backend API URL for production"
git push origin main
```

## Step 4: Deploy Frontend to Netlify 🌐

1. **Go to Netlify**: Visit [app.netlify.com](https://app.netlify.com) and sign up/login
2. **Import Project**:
   - Click "Add new site" → "Import an existing project"
   - Click "Deploy with GitHub"
   - Authorize Netlify to access your GitHub
   - Select your repository: `nico-mannarelli/bird-camera`
3. **Configure Build Settings**:
   - **Base directory**: (leave empty)
   - **Build command**: (leave empty)
   - **Publish directory**: `.` (just a dot - current directory)
4. **Deploy**:
   - Click "Deploy site"
   - Wait 1-2 minutes for deployment
5. **Get Your Site URL**:
   - Netlify provides a URL like: `https://random-name-12345.netlify.app`
   - You can customize it in Site settings → Domain management

## Step 5: Test Your Deployment ✅

1. Visit your Netlify URL
2. Upload a bird image
3. **First request will be slow** (30-60 seconds) - the model is downloading and loading
4. Subsequent requests should be faster (~1-2 seconds)

## Troubleshooting 🔧

### Backend Issues

**"Application failed to respond"**
- Check Railway logs: Go to your service → "Deployments" → Click latest → View logs
- Common issues:
  - Model download failing (check Google Drive file ID in `api.py`)
  - Out of memory (Railway free tier has 512MB, may need upgrade)
  - Timeout (first request is slow, increase timeout in Railway settings)

**"Module not found" errors**
- Make sure `requirements.txt` includes all dependencies
- Check Railway logs for missing packages

### Frontend Issues

**CORS errors in browser console**
- Make sure `flask-cors` is in `requirements.txt`
- Verify backend URL in `script.js` is correct
- Check that backend is actually running (visit backend URL + `/health`)

**"Failed to fetch" errors**
- Check backend URL in `script.js`
- Make sure backend is deployed and running
- Check browser console for detailed error

### Model Download Issues

If model download fails:
1. Check Railway logs
2. Verify Google Drive file ID in `api.py` (line 29)
3. Make sure file is publicly accessible on Google Drive

## Cost Estimates 💰

- **Railway**: Free tier includes $5/month credit (usually enough for small apps)
- **Netlify**: Free tier is generous (100GB bandwidth, 300 build minutes/month)

## Next Steps 🚀

- Customize your Netlify domain name
- Set up custom domain (optional)
- Monitor usage on both platforms
- Consider adding error tracking (Sentry, etc.)

