# 🚀 Autopilot Pro - Deployment Guide

## 📊 Deployment Options Comparison

| Option | Cost | Ease | GPU Support | Always On | Best For |
|--------|------|------|-------------|-----------|----------|
| **Hugging Face Spaces** | FREE | ⭐⭐⭐⭐⭐ | ✅ (paid) | ✅ | Quick demo, free hosting |
| **Gradio Share Links** | FREE | ⭐⭐⭐⭐⭐ | ✅ | ❌ 72hrs | Temporary sharing |
| **Google Colab** | FREE | ⭐⭐⭐⭐ | ✅ Free | ❌ 12hrs | Testing, development |
| **Railway.app** | FREE/$5 | ⭐⭐⭐⭐ | ❌ | ✅ | Small projects |
| **Render.com** | FREE | ⭐⭐⭐⭐ | ❌ | ✅ | Web services |
| **AWS/GCP/Azure** | $$$ | ⭐⭐⭐ | ✅ | ✅ | Production, enterprise |
| **DigitalOcean** | $5-20 | ⭐⭐⭐ | ❌ | ✅ | Custom VPS |
| **Docker + Cloud** | $$ | ⭐⭐⭐ | ✅ | ✅ | Scalable, professional |

---

## 🏆 **RECOMMENDED: Hugging Face Spaces** (FREE & BEST)

### Why Hugging Face Spaces?
- ✅ **100% FREE** for public projects
- ✅ **Always running** (permanent URLs)
- ✅ **Built for ML models** (optimized for YOLO)
- ✅ **GPU available** (upgrade option)
- ✅ **Easy deployment** (Git-based)
- ✅ **Professional URLs**: `https://huggingface.co/spaces/YOUR_USERNAME/autopilot-pro`
- ✅ **Auto-restart** on crashes
- ✅ **Built-in monitoring**

### Deployment Steps:

#### 1. Create Hugging Face Account
- Go to https://huggingface.co/join
- Sign up (free)
- Verify email

#### 2. Create New Space
- Go to https://huggingface.co/new-space
- **Name**: `autopilot-pro`
- **License**: Choose appropriate license
- **SDK**: Select `Gradio`
- **Hardware**: Start with CPU (free), upgrade to GPU if needed

#### 3. Prepare Your Project

**I'll create the deployment files for you now...**

---

## 📁 Deployment Files Created ✅

I've created all necessary files:

1. ✅ `app.py` - Unified Gradio app with all 5 models in tabs
2. ✅ `requirements.txt` - All dependencies
3. ✅ `.gitattributes` - Git LFS configuration for model files
4. ✅ `Dockerfile` - Docker container configuration
5. ✅ `docker-compose.yml` - Docker Compose for easy deployment

---

## 🚀 Option 1: Hugging Face Spaces (RECOMMENDED - FREE)

### Step-by-Step Deployment:

#### 1. Install Git LFS (Large File Storage)

**On Mac:**
```bash
brew install git-lfs
git lfs install
```

**On Ubuntu/Debian:**
```bash
sudo apt-get install git-lfs
git lfs install
```

**On Windows:**
- Download from: https://git-lfs.github.com/
- Run installer
- Open cmd: `git lfs install`

#### 2. Create Hugging Face Account & Space

1. Go to https://huggingface.co/join
2. Sign up (free account)
3. Go to https://huggingface.co/new-space
4. Fill in:
   - **Space name**: `autopilot-pro` (or your choice)
   - **License**: Apache 2.0 or MIT
   - **SDK**: Select `Gradio`
   - **Hardware**: CPU (free) or GPU (paid upgrade)
   - **Visibility**: Public (free) or Private (Pro account)

#### 3. Clone Your New Space

```bash
cd /Users/muhammadsharjeel/Documents/MODEL

# Clone the empty space (replace USERNAME with your HF username)
git clone https://huggingface.co/spaces/USERNAME/autopilot-pro
cd autopilot-pro
```

#### 4. Copy Project Files to Space

```bash
# Copy main files
cp ../Autopilot_Pro/app.py .
cp ../Autopilot_Pro/requirements.txt .
cp ../Autopilot_Pro/.gitattributes .

# Copy model folders (with weights)
cp -r ../Autopilot_Pro/LTV_HTV_Model .
cp -r ../Autopilot_Pro/Pedestrian_Model .
cp -r ../Autopilot_Pro/Traffic_Light_Model .
cp -r ../Autopilot_Pro/TRAFFIC_SIGN_MODEL .

# Optional: Copy UI for local reference
cp -r ../Autopilot_Pro/UI .
```

#### 5. Create README for Space

Create `README.md` in the space folder:

```markdown
---
title: Autopilot Pro
emoji: 🚗
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: "4.0.0"
app_file: app.py
pinned: false
---

# 🚗 Autopilot Pro - AI Detection System

Multi-model YOLO-based detection system for autonomous driving applications.

## Features

- 🚙 LTV/HTV Detection
- 🚶 Pedestrian Detection
- 🚦 Traffic Light Detection
- 🚸 Traffic Sign Detection (33+ types)
- 🤖 Combined Detection (All models)

## Usage

Upload an image and select a model to see detections!
```

#### 6. Track Model Files with Git LFS

```bash
# Track all .pt model files with LFS
git lfs track "*.pt"
git add .gitattributes
```

#### 7. Push to Hugging Face

```bash
# Add all files
git add .

# Commit
git commit -m "Initial deployment of Autopilot Pro"

# Push to Hugging Face (may take time for large models)
git push
```

#### 8. Wait for Build

- Hugging Face will automatically build your space
- Monitor at: `https://huggingface.co/spaces/USERNAME/autopilot-pro`
- First build takes 5-10 minutes
- Once done, you'll get a permanent URL!

#### 9. Share Your Live App! 🎉

Your app will be live at:
```
https://USERNAME-autopilot-pro.hf.space
```

Or:
```
https://huggingface.co/spaces/USERNAME/autopilot-pro
```

---

## 🚀 Option 2: Quick Test with Gradio Share (72 hours)

If you want to test immediately without deployment:

```bash
cd /Users/muhammadsharjeel/Documents/MODEL/Autopilot_Pro
python app.py
```

Gradio will generate a public link like:
```
https://xxxxxxxxxxxx.gradio.live
```

**Limitations:**
- Link expires after 72 hours
- Requires your computer to stay on
- Limited to 100 concurrent users

---

## 🐳 Option 3: Docker Deployment (Advanced)

### For Any Cloud Provider (AWS, GCP, Azure, DigitalOcean)

#### Build and Test Locally:

```bash
cd /Users/muhammadsharjeel/Documents/MODEL/Autopilot_Pro

# Build Docker image
docker build -t autopilot-pro:latest .

# Run locally
docker run -p 7860:7860 autopilot-pro:latest

# Or use docker-compose
docker-compose up -d
```

Visit: http://localhost:7860

#### Deploy to Cloud:

**DigitalOcean App Platform:**
1. Create account: https://www.digitalocean.com
2. Connect GitHub/GitLab
3. Select Dockerfile deployment
4. Choose $5/month plan
5. Deploy! (auto-restarts, always-on)

**Railway.app:**
1. Go to https://railway.app
2. New Project → Deploy from GitHub
3. Detects Dockerfile automatically
4. Free tier: $5/month credit
5. Auto-deployed on push

**Render.com:**
1. Go to https://render.com
2. New Web Service
3. Connect repository
4. Select Docker
5. Free tier available

---

## 📊 Option 4: Google Colab (Free GPU, 12 hours)

Create notebook:

```python
# Install dependencies
!pip install gradio ultralytics opencv-python pillow

# Clone your repository
!git clone https://github.com/YOUR_USERNAME/Autopilot_Pro.git
%cd Autopilot_Pro

# Run app
!python app.py
```

**Limitations:**
- Session expires after 12 hours
- Must manually restart
- Good for testing/demos

---

## 🎯 Comparison for Your Use Case

### Best Options:

#### **For Free + Always On:**
→ **Hugging Face Spaces** (WINNER!)
- ✅ Completely free
- ✅ Always running
- ✅ Professional URL
- ✅ Built for ML models
- ✅ Easy updates via Git

#### **For Quick Demo:**
→ **Gradio Share Links**
- ✅ Instant (no signup)
- ✅ Public URL in seconds
- ❌ Expires in 72 hours

#### **For Production/Commercial:**
→ **Docker + Railway/Render**
- ✅ Professional hosting
- ✅ Custom domain
- ✅ Scalable
- ✅ $5-20/month

---

## 🔧 Post-Deployment: Update UI URLs

After deployment, update your local UI to point to deployed URLs:

**Edit `UI/home.html`:**

```javascript
// Replace localhost URLs with your deployed URLs
onclick="loadGradioApp('https://YOUR_USERNAME-autopilot-pro.hf.space', '🚙 LTV/HTV Detection')"
```

Or serve the UI separately and have it embed the deployed Gradio iframes.

---

## 📈 Monitoring & Maintenance

### Hugging Face Spaces:

**View Logs:**
```
https://huggingface.co/spaces/USERNAME/autopilot-pro/logs
```

**Check Status:**
```
https://huggingface.co/spaces/USERNAME/autopilot-pro/settings
```

**Update Models:**
```bash
# In your local space clone
git pull
# Make changes
git add .
git commit -m "Update model"
git push
# Space rebuilds automatically
```

### Docker Deployment:

**Check Logs:**
```bash
docker logs autopilot-pro
```

**Restart:**
```bash
docker-compose restart
```

**Update:**
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## 🎨 Customization for Deployment

### Reduce Model Size (Optional):

If models are too large (>5GB total), you can:

1. **Quantize models** (reduce precision)
2. **Use smaller YOLO variants** (YOLOv8n instead of YOLOv8x)
3. **Deploy only essential models**

### Optimize for Speed:

In `app.py`, adjust:

```python
# Use smaller image sizes
model(img_array, imgsz=640)  # Instead of default 1280

# Reduce confidence threshold
confidence_threshold=0.5  # Fewer detections = faster
```

---

## 💡 Pro Tips

1. **Start with Hugging Face Spaces** (easiest & free)
2. **Test with Gradio Share** first to verify everything works
3. **Use Docker** for production deployments
4. **Enable GPU** on HF Spaces if models are slow (paid upgrade)
5. **Monitor usage** to stay within free tier limits
6. **Version your models** using Git tags
7. **Add examples** to Gradio interface for better UX
8. **Enable queue** in Gradio for high traffic

---

## 🆘 Troubleshooting Deployment

### Issue: Models too large for Git

**Solution**: Git LFS (already configured in `.gitattributes`)
```bash
git lfs install
git lfs track "*.pt"
```

### Issue: Out of memory

**Solution**: Reduce batch size or use CPU
```python
# In app.py
model(img_array, device='cpu')
```

### Issue: Slow inference

**Solution**: 
1. Enable GPU (HF Spaces paid tier)
2. Reduce image size
3. Use quantized models

### Issue: Space build fails

**Solution**: Check logs at HF Space → Settings → Logs
Common fixes:
- Update Python version in Dockerfile
- Pin dependency versions in requirements.txt
- Ensure all model files are tracked with LFS

---

## 📞 Next Steps

1. **Choose your deployment method** (I recommend Hugging Face Spaces!)
2. **Follow the step-by-step guide** above
3. **Test your deployed app**
4. **Share the URL** with users!

---

## 🎉 Your App Will Be Live!

After deployment, you'll have:
- ✅ **Permanent URL** (e.g., `https://username-autopilot-pro.hf.space`)
- ✅ **Always running** (24/7 availability)
- ✅ **Auto-restart** on crashes
- ✅ **Free hosting** (HF Spaces)
- ✅ **Professional appearance**
- ✅ **Easy updates** via Git push

---

**Ready to deploy? Start with Option 1 (Hugging Face Spaces)! 🚀**

Need help? Check the [Hugging Face Spaces documentation](https://huggingface.co/docs/hub/spaces-overview)

