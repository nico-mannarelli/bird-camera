# Netlify Deployment Guide (All-in-One)

This guide shows you how to deploy everything on Netlify using Netlify Functions.

## ⚠️ Important Limitations

**Netlify Functions have constraints:**
- **Free tier**: 10-second timeout (may not be enough for model loading)
- **Pro tier**: 26-second timeout (better, but still tight)
- **Function size**: Limited to 50MB unzipped
- **Cold starts**: First request after inactivity can be slow

**Recommendation**: If you have Netlify Pro, this will work better. Otherwise, consider the Railway backend option.

## 🚀 Deployment Steps

### 1. Prepare Your Repository

Make sure all files are committed and pushed:
```bash
git add .
git commit -m "Add Netlify Functions support"
git push origin main
```

### 2. Deploy to Netlify

1. **Go to Netlify**: Visit [app.netlify.com](https://app.netlify.com)
2. **Import Project**:
   - Click "Add new site" → "Import an existing project"
   - Click "Deploy with GitHub"
   - Authorize Netlify
   - Select your repository: `nico-mannarelli/bird-camera`
3. **Configure Build Settings**:
   - **Base directory**: (leave empty)
   - **Build command**: (leave empty)
   - **Publish directory**: `.` (current directory)
4. **Advanced Settings** (click "Show advanced"):
   - **Functions directory**: `netlify/functions`
5. **Deploy**:
   - Click "Deploy site"
   - Wait for deployment (5-10 minutes first time)

### 3. Install Python Dependencies

Netlify Functions need Python dependencies. You have two options:

#### Option A: Using Netlify Build Plugin (Recommended)

1. Go to your site settings → Build & deploy → Plugins
2. Install "Python Runtime" plugin
3. Or add to `netlify.toml`:
```toml
[[plugins]]
  package = "@netlify/plugin-python"
```

#### Option B: Manual Setup

Netlify will automatically install dependencies from `netlify/functions/requirements.txt` if you have the Python plugin installed.

### 4. Test Your Deployment

1. Visit your Netlify URL
2. Upload a bird image
3. **First request will be VERY slow** (30-60+ seconds):
   - Model download (~23MB)
   - Model loading
   - May timeout on free tier
4. Subsequent requests should be faster (if function stays warm)

## 🔧 Configuration

### Timeout Settings

If you have Netlify Pro, you can increase the timeout in `netlify.toml`:
```toml
[functions.detect]
  timeout = 26  # Max for Pro tier
```

### Environment Variables

If needed, add in Netlify dashboard:
- Site settings → Environment variables

## 🐛 Troubleshooting

### "Function execution timeout"

**Problem**: Request takes longer than 10 seconds (free) or 26 seconds (pro)

**Solutions**:
1. Upgrade to Netlify Pro for 26s timeout
2. Use Railway/Render backend instead (no timeout limits)
3. Optimize model loading (pre-warm function)

### "Module not found" errors

**Problem**: Python dependencies not installed

**Solutions**:
1. Make sure `netlify/functions/requirements.txt` exists
2. Install Python plugin in Netlify
3. Check build logs for installation errors

### Model download fails

**Problem**: Google Drive download times out or fails

**Solutions**:
1. Check Google Drive file ID in `netlify/functions/detect.py`
2. Ensure file is publicly accessible
3. Consider hosting model on S3 or CDN

### CORS errors

**Problem**: Browser blocks requests

**Solution**: Already handled in function code with CORS headers

## 💡 Optimization Tips

1. **Pre-warm function**: Set up a cron job to ping `/health` endpoint
2. **Model caching**: Model is cached in `/tmp` (persists across invocations)
3. **Image optimization**: Compress images before sending to reduce payload size
4. **Consider edge functions**: For faster cold starts (but limited Python support)

## 📊 Cost Considerations

- **Netlify Free**: 125k function invocations/month, 10s timeout
- **Netlify Pro**: $19/month, 500k invocations, 26s timeout
- **Bandwidth**: 100GB free, then $0.15/GB

## 🔄 Alternative: Hybrid Approach

If Netlify Functions don't work well, you can:
1. Keep frontend on Netlify (works great!)
2. Deploy backend to Railway/Render (no timeout limits)
3. Update `script.js` to point to external backend

See `DEPLOY_STEPS.md` for Railway backend setup.

