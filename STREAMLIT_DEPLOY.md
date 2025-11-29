# 🚀 Streamlit Cloud Deployment Guide

Your Streamlit app is ready to deploy! Streamlit Cloud handles ML models really well.

## Quick Deployment Steps

### 1. Prepare Your Repository

Make sure everything is committed:
```bash
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

### 2. Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**: Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign up/login with GitHub

2. **Deploy App**:
   - Click "New app"
   - Select your repository: `nico-mannarelli/bird-camera`
   - **Main file path**: `app.py`
   - **Python version**: 3.10 or 3.11 (auto-detected)
   - Click "Deploy"

3. **Wait for Deployment** (5-10 minutes):
   - Streamlit will install dependencies
   - First deployment takes longer
   - Watch the logs for progress

4. **Your App is Live!**
   - Streamlit provides a URL like: `https://your-app-name.streamlit.app`
   - Share this URL with anyone!

## ✅ What Streamlit Cloud Handles Automatically

- ✅ Python environment setup
- ✅ Dependency installation (from requirements.txt)
- ✅ System libraries (OpenCV, PyTorch work out of the box)
- ✅ Model downloading (your gdown code works)
- ✅ Auto-deploys on git push
- ✅ Free hosting

## 📝 Important Notes

### Model Download
- First user will trigger model download (~23MB from Google Drive)
- Takes 10-30 seconds on first load
- Model is cached for subsequent requests

### Performance
- First request: ~30-60 seconds (model download + load)
- Subsequent requests: ~1-2 seconds (model cached)
- Inference time: ~300ms per image

### Free Tier Limits
- ✅ Unlimited apps
- ✅ Unlimited usage
- ⚠️ Apps sleep after 1 hour of inactivity (wake up on next request)

## 🔧 Configuration Files

Your app uses:
- `app.py` - Main Streamlit app
- `requirements.txt` - Python dependencies
- `best.pt` - Model file (auto-downloaded from Google Drive)

## 🐛 Troubleshooting

### "Module not found" errors
- Check `requirements.txt` has all dependencies
- Make sure `streamlit` is in requirements.txt

### Model download fails
- Verify Google Drive file ID in `app.py` (line 21)
- Ensure file is publicly accessible
- Check Streamlit logs for download errors

### App is slow
- First request is always slow (model download)
- Subsequent requests should be fast
- Check Streamlit logs for any errors

## 🎉 You're Done!

Once deployed, your app will be live at:
`https://your-app-name.streamlit.app`

The app will:
1. Download model on first use
2. Allow users to upload bird images
3. Show detection results with bounding boxes
4. Display species names and confidence scores

## 📚 Next Steps (Optional)

- Customize the Streamlit theme
- Add more features to the app
- Share your app URL
- Monitor usage in Streamlit Cloud dashboard

---

**That's it!** Streamlit Cloud makes ML deployment super easy. Your app should work perfectly! 🎉

