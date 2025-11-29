# 🚀 Quick Netlify Deployment

Your app is now configured to deploy entirely on Netlify!

## ⚡ Quick Start

1. **Push to GitHub** (if not already):
   ```bash
   git add .
   git commit -m "Configure for Netlify deployment"
   git push origin main
   ```

2. **Deploy on Netlify**:
   - Go to [app.netlify.com](https://app.netlify.com)
   - Click "Add new site" → "Import an existing project"
   - Connect GitHub → Select `nico-mannarelli/bird-camera`
   - Build settings:
     - Publish directory: `.`
     - Functions directory: `netlify/functions`
   - Click "Deploy site"

3. **Wait for deployment** (5-10 minutes first time)

4. **Test it!** Visit your Netlify URL and upload a bird image

## ⚠️ Important Notes

### Timeout Limitations
- **Free tier**: 10-second timeout (may timeout on first request)
- **Pro tier**: 26-second timeout (better, but still tight)
- First request downloads & loads model (~30-60 seconds) - **will likely timeout on free tier**

### What Happens
1. First request: Downloads model (23MB) + loads it → **May timeout**
2. Subsequent requests: Uses cached model → **Should work** (if function stays warm)

### Recommendations

**Option 1: Try Netlify (Current Setup)**
- Works if you have Pro tier (26s timeout)
- Free tier will likely timeout on first request
- Subsequent requests should work if function stays warm

**Option 2: Hybrid (Recommended)**
- Frontend on Netlify ✅ (works great!)
- Backend on Railway/Render (no timeout limits)
- Update `script.js` to point to external backend

See `DEPLOY_STEPS.md` for Railway backend setup.

## 📁 Project Structure

```
bird-cam-project/
├── index.html          # Frontend
├── style.css           # Styles
├── script.js           # Frontend JS (uses Netlify Functions)
├── netlify/
│   └── functions/
│       ├── detect.py   # Bird detection function
│       ├── health.py   # Health check
│       └── requirements.txt
├── netlify.toml        # Netlify configuration
└── package.json        # For Python plugin
```

## 🔧 Troubleshooting

**Function timeout?**
- Upgrade to Netlify Pro, or
- Use Railway backend (see `DEPLOY_STEPS.md`)

**Module not found?**
- Check that `@netlify/plugin-python` is installed
- Verify `netlify/functions/requirements.txt` exists

**Model download fails?**
- Check Google Drive file ID in `netlify/functions/detect.py`
- Verify file is publicly accessible

## 📚 More Info

- Full deployment guide: `NETLIFY_DEPLOYMENT.md`
- Railway backend option: `DEPLOY_STEPS.md`
- Quick start: `QUICK_START.md`

