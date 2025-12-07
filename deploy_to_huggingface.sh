#!/bin/bash
# Automated Deployment Script for Hugging Face Spaces
# =====================================================

echo "🚀 Autopilot Pro - Hugging Face Deployment Helper"
echo "=================================================="
echo ""

# Check if Git LFS is installed
if ! command -v git-lfs &> /dev/null; then
    echo "❌ Git LFS is not installed!"
    echo "📥 Installing Git LFS..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install git-lfs
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        sudo apt-get update && sudo apt-get install -y git-lfs
    else
        echo "⚠️  Please install Git LFS manually: https://git-lfs.github.com/"
        exit 1
    fi
    
    git lfs install
fi

echo "✅ Git LFS is installed"
echo ""

# Get Hugging Face username
read -p "Enter your Hugging Face username: " HF_USERNAME

if [ -z "$HF_USERNAME" ]; then
    echo "❌ Username cannot be empty!"
    exit 1
fi

# Get space name
read -p "Enter space name (default: autopilot-pro): " SPACE_NAME
SPACE_NAME=${SPACE_NAME:-autopilot-pro}

echo ""
echo "📦 Configuration:"
echo "   Username: $HF_USERNAME"
echo "   Space: $SPACE_NAME"
echo "   URL: https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME"
echo ""

read -p "Proceed with deployment? (y/n): " CONFIRM

if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo "❌ Deployment cancelled"
    exit 0
fi

echo ""
echo "🔄 Step 1: Creating deployment directory..."

DEPLOY_DIR="../${SPACE_NAME}_hf_space"
mkdir -p "$DEPLOY_DIR"
cd "$DEPLOY_DIR" || exit 1

echo "✅ Created: $DEPLOY_DIR"
echo ""

echo "🔄 Step 2: Cloning Hugging Face Space..."

HF_SPACE_URL="https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME"

if git clone "$HF_SPACE_URL" .; then
    echo "✅ Space cloned successfully"
else
    echo "❌ Failed to clone space. Make sure:"
    echo "   1. You've created the space at: https://huggingface.co/new-space"
    echo "   2. Your username is correct: $HF_USERNAME"
    echo "   3. Space name is correct: $SPACE_NAME"
    echo "   4. You're logged in: git config --global credential.helper store"
    exit 1
fi

echo ""
echo "🔄 Step 3: Copying project files..."

# Copy main files
cp ../Autopilot_Pro/app.py . || exit 1
cp ../Autopilot_Pro/requirements.txt . || exit 1
cp ../Autopilot_Pro/.gitattributes . || exit 1
cp ../Autopilot_Pro/config.py . || exit 1

# Copy model folders
cp -r ../Autopilot_Pro/LTV_HTV_Model . || exit 1
cp -r ../Autopilot_Pro/Pedestrian_Model . || exit 1
cp -r ../Autopilot_Pro/Traffic_Light_Model . || exit 1
cp -r ../Autopilot_Pro/TRAFFIC_SIGN_MODEL . || exit 1

echo "✅ Files copied"
echo ""

echo "🔄 Step 4: Creating README.md..."

cat > README.md << 'EOF'
---
title: Autopilot Pro
emoji: 🚗
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: "4.0.0"
app_file: app.py
pinned: false
license: mit
---

# 🚗 Autopilot Pro - AI Detection System

Multi-model YOLO-based detection system for autonomous driving applications.

## 🎯 Features

- 🚙 **LTV/HTV Detection**: Light and Heavy Traffic Vehicles
- 🚶 **Pedestrian Detection**: Identify people in scenes  
- 🚦 **Traffic Light Detection**: Red, Yellow, Green light recognition
- 🚸 **Traffic Sign Detection**: 33+ traffic sign types
- 🤖 **Combined Detection**: All models working together

## 🚀 How to Use

1. Select a model tab
2. Upload an image
3. Adjust confidence threshold
4. View detection results!

## 📊 Model Information

| Model | Purpose | Classes |
|-------|---------|---------|
| LTV/HTV | Vehicle detection | Cars, Trucks, Buses |
| Pedestrian | People detection | Pedestrians |
| Traffic Light | Signal recognition | Red, Yellow, Green |
| Traffic Sign | Sign classification | 33+ sign types |

## 🔧 Technical Details

- **Framework**: YOLOv8 (Ultralytics)
- **Interface**: Gradio
- **Language**: Python 3.10
- **GPU**: Optional (CPU supported)

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Credits

Built with ❤️ using YOLO and Gradio
EOF

echo "✅ README created"
echo ""

echo "🔄 Step 5: Setting up Git LFS..."

git lfs track "*.pt"
git add .gitattributes

echo "✅ Git LFS configured"
echo ""

echo "🔄 Step 6: Adding all files to Git..."

git add .

echo "✅ Files staged"
echo ""

echo "🔄 Step 7: Creating commit..."

git commit -m "🚀 Initial deployment of Autopilot Pro with all models"

echo "✅ Committed"
echo ""

echo "🔄 Step 8: Pushing to Hugging Face (this may take a while for large models)..."

if git push; then
    echo ""
    echo "✅ ✅ ✅ DEPLOYMENT SUCCESSFUL! ✅ ✅ ✅"
    echo ""
    echo "🎉 Your Autopilot Pro is now deploying!"
    echo ""
    echo "📍 URLs:"
    echo "   Space: https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME"
    echo "   Live: https://$HF_USERNAME-$SPACE_NAME.hf.space"
    echo ""
    echo "⏳ Build Status: https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME/logs"
    echo ""
    echo "📝 Note: First build takes 5-10 minutes. Monitor the logs link above."
    echo ""
    echo "🎊 Once built, your app will be live and accessible 24/7!"
    echo ""
else
    echo ""
    echo "❌ Push failed. Common issues:"
    echo "   1. Authentication: Run 'git config --global credential.helper store' and try again"
    echo "   2. Large files: Make sure Git LFS is properly installed"
    echo "   3. Network: Check your internet connection"
    echo ""
    echo "📝 Manual steps:"
    echo "   cd $DEPLOY_DIR"
    echo "   git push"
    exit 1
fi

# Open space in browser
if command -v open &> /dev/null; then
    # macOS
    open "https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME"
elif command -v xdg-open &> /dev/null; then
    # Linux
    xdg-open "https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME"
fi

echo "🌐 Opening space in browser..."
echo ""
echo "✨ Deployment complete! ✨"

