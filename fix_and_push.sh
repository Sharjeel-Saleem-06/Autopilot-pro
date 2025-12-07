#!/bin/bash
# Quick Fix Script - Complete Your HF Deployment
# ==============================================

echo "🔧 Fixing authentication and completing deployment..."
echo ""

# Check if we're in the deployment directory
if [ ! -d "../autopilot-pro_hf_space" ]; then
    echo "❌ Deployment directory not found!"
    echo "Run ./deploy_to_huggingface.sh first"
    exit 1
fi

cd ../autopilot-pro_hf_space || exit 1

echo "📍 Current directory: $(pwd)"
echo ""

echo "🔐 Step 1: Get Your Hugging Face Access Token"
echo "─────────────────────────────────────────────"
echo ""
echo "1. Go to: https://huggingface.co/settings/tokens"
echo "2. Click: 'New token'"
echo "3. Name: 'autopilot-deploy'"
echo "4. Type: Select 'Write'"
echo "5. Click: 'Generate'"
echo "6. COPY THE TOKEN (starts with hf_...)"
echo ""
echo "Example token: hf_AbCdEfGhIjKlMnOpQrStUvWxYz1234567890"
echo ""

read -p "Have you created and copied your token? (y/n): " TOKEN_READY

if [ "$TOKEN_READY" != "y" ] && [ "$TOKEN_READY" != "Y" ]; then
    echo ""
    echo "❌ Please create your access token first, then run this script again."
    echo ""
    echo "Quick link: https://huggingface.co/settings/tokens"
    exit 0
fi

echo ""
echo "✅ Great! Let's configure Git..."
echo ""

# Configure credential storage
git config --global credential.helper store
echo "✅ Git will remember your token"
echo ""

echo "🚀 Step 2: Pushing to Hugging Face..."
echo "────────────────────────────────────"
echo ""
echo "You will be prompted for:"
echo "  Username: sharry121"
echo "  Password: [PASTE YOUR TOKEN HERE - not your password!]"
echo ""
echo "⚠️  IMPORTANT: When prompted for 'Password', paste your ACCESS TOKEN!"
echo "   (It starts with: hf_...)"
echo ""

read -p "Ready to push? (y/n): " PUSH_READY

if [ "$PUSH_READY" != "y" ] && [ "$PUSH_READY" != "Y" ]; then
    echo ""
    echo "No problem! You can push manually later:"
    echo ""
    echo "  cd $(pwd)"
    echo "  git push"
    echo ""
    exit 0
fi

echo ""
echo "🔄 Pushing to Hugging Face..."
echo ""

if git push; then
    echo ""
    echo "✅ ✅ ✅ SUCCESS! ✅ ✅ ✅"
    echo ""
    echo "🎉 Your Autopilot Pro is now deploying!"
    echo ""
    echo "📍 Your URLs:"
    echo "   Space: https://huggingface.co/spaces/sharry121/autopilot-pro"
    echo "   Live:  https://sharry121-autopilot-pro.hf.space"
    echo ""
    echo "⏳ Build Status: https://huggingface.co/spaces/sharry121/autopilot-pro/logs"
    echo ""
    echo "📝 Note:"
    echo "   - First build takes 5-10 minutes"
    echo "   - Monitor progress at the logs link above"
    echo "   - Once built, your app will be live 24/7!"
    echo ""
    
    # Try to open in browser
    if command -v open &> /dev/null; then
        open "https://huggingface.co/spaces/sharry121/autopilot-pro"
    fi
    
    echo "🌐 Opening space in browser..."
    echo ""
    echo "✨ Deployment complete! ✨"
    
else
    echo ""
    echo "❌ Push failed."
    echo ""
    echo "Common reasons:"
    echo "  1. You entered your HF password instead of token"
    echo "  2. Token doesn't have 'Write' permission"
    echo "  3. Token was typed incorrectly"
    echo ""
    echo "Try again:"
    echo "  1. Get token: https://huggingface.co/settings/tokens"
    echo "  2. Make sure it has 'Write' permission"
    echo "  3. Run: git push"
    echo "  4. Username: sharry121"
    echo "  5. Password: [paste your hf_... token]"
    echo ""
fi

