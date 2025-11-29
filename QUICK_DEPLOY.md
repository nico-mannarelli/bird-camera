# ⚡ Quick Deployment Checklist

## 🚂 Step 1: Deploy Backend (Railway) - 5 minutes

1. Go to [railway.app](https://railway.app) → Sign up/login
2. Click "New Project" → "Deploy from GitHub repo"
3. Select `nico-mannarelli/bird-camera`
4. Wait for deployment (5-10 min)
5. **Copy your Railway URL** from Settings → Domains
   - Looks like: `https://your-app.up.railway.app`

## 🌐 Step 2: Update Frontend - 2 minutes

1. Open `script.js`
2. Find line 7, replace with your Railway URL:
   ```javascript
   : 'https://your-actual-railway-url.up.railway.app';
   ```
3. Save, commit, push:
   ```bash
   git add script.js
   git commit -m "Add Railway backend URL"
   git push
   ```

## ✅ Step 3: Test

1. Visit your Netlify site
2. Upload a bird image
3. Should work! 🎉

## 📚 Full guide: `RAILWAY_DEPLOY.md`

