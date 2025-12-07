# 📖 Autopilot Pro - Complete Usage Guide

## 🚀 Quick Start (3 Steps)

### Step 1: Navigate to Project
```bash
cd /path/to/Autopilot_Pro
```

### Step 2: Launch Everything
```bash
python launch_all.py
```

### Step 3: Use the UI
The browser will open automatically at `UI/home.html`

**That's it! You're ready to go!** 🎉

---

## 📺 What You'll See

### When You Run `launch_all.py`:

```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║              🚗  AUTOPILOT PRO LAUNCHER  🚗              ║
║                                                           ║
║         Multi-Model AI Detection System v1.0             ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

🔍 Checking dependencies...

  ✅ Gradio (Web Interface)
  ✅ Ultralytics YOLO
  ✅ OpenCV
  ✅ Pillow
  ✅ NumPy
  ✅ Requests

✅ All dependencies are installed!

📡 Starting Gradio Servers in Parallel...

⚡ Phase 1: Starting all processes...
  [1/5] 🚀 Launching 🚙 LTV/HTV Detection...
  [2/5] 🚀 Launching 🚶 Pedestrian Detection...
  [3/5] 🚀 Launching 🚦 Traffic Light Detection...
  [4/5] 🚀 Launching 🚸 Traffic Sign Detection...
  [5/5] 🚀 Launching 🤖 Autopilot Pro (Combined)...

⏳ Phase 2: Waiting for servers to be ready...
   (Models are loading into memory - usually takes 30-60 seconds)

  [12s] ⏳⏳⏳⏳⏳ (0/5 ready)
  ✅ 🚙 LTV/HTV Detection is ready! (Port: 7860) [24s]
  ✅ 🚶 Pedestrian Detection is ready! (Port: 7861) [28s]
  ✅ 🚦 Traffic Light Detection is ready! (Port: 7862) [35s]
  ✅ 🚸 Traffic Sign Detection is ready! (Port: 7869) [42s]
  ✅ 🤖 Autopilot Pro (Combined) is ready! (Port: 7868) [58s]

============================================================

✅ Successfully launched: 5/5 servers in 58s

============================================================

🌐 Server Information:
────────────────────────────────────────────────────────────
  🚙 LTV/HTV Detection            http://127.0.0.1:7860
  🚶 Pedestrian Detection         http://127.0.0.1:7861
  🚦 Traffic Light Detection      http://127.0.0.1:7862
  🚸 Traffic Sign Detection       http://127.0.0.1:7869
  🤖 Autopilot Pro (Combined)     http://127.0.0.1:7868
────────────────────────────────────────────────────────────

🌐 Opening Autopilot Pro UI in browser...
✓ UI opened: /path/to/UI/home.html

╔═══════════════════════════════════════════════════════════╗
║                   📖 INSTRUCTIONS                         ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  ✓ All Gradio servers are now running!                   ║
║  ✓ The UI should open automatically in your browser      ║
║                                                           ║
║  💡 Usage:                                                ║
║     • Click any model button in the left sidebar         ║
║     • Upload images or use live camera detection         ║
║     • View performance metrics in the tabs               ║
║                                                           ║
║  🛑 To stop all servers:                                  ║
║     • Press Ctrl+C in this terminal                      ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

⏳ Press Ctrl+C to stop all servers and exit...
```

---

## 🎨 UI Features

### Home Page
When you first open the UI, you'll see:
- 🏠 Animated landing page
- 🚗 Moving cars and vehicles
- 🚦 Traffic lights
- 🏢 Buildings
- 📊 Project statistics

### Left Sidebar Navigation

**5 Main Sections:**

1. **🚙 LTV/HTV DETECTION** (Expandable)
   - MODEL TESTING → Opens Gradio interface
   - MODEL PERFORMANCE → Shows training metrics

2. **🚶 PEDESTRIAN DETECTION** (Expandable)
   - MODEL TESTING → Opens Gradio interface
   - MODEL PERFORMANCE → Shows training metrics

3. **🚦 TRAFFIC LIGHT DETECTION** (Expandable)
   - MODEL TESTING → Opens Gradio interface
   - MODEL PERFORMANCE → Shows training metrics

4. **🚸 TRAFFIC SIGN DETECTION** (Expandable)
   - MODEL TESTING → Opens Gradio interface

5. **🤖 AUTOPILOT PRO** (Expandable)
   - MODEL TESTING → All models combined

---

## 🔄 Loading Animation

### When You Click "MODEL TESTING":

**Phase 1: Loading Screen Appears**
```
┌─────────────────────────────┐
│                             │
│        [Spinning Circle]    │
│                             │
│  🚀 Loading 🚙 LTV/HTV      │
│     Detection...            │
│                             │
│  Please wait while the      │
│  model initializes          │
│                             │
│      • • •                  │
│  (animated dots)            │
│                             │
└─────────────────────────────┘
```

**Phase 2: Model Interface Loads**
- Smooth fade-in transition
- Gradio interface appears
- Ready to use!

**If Connection Fails:**
```
┌─────────────────────────────┐
│           ⚠️                 │
│                             │
│     Connection Issue        │
│                             │
│  The model server may not   │
│  be running.                │
│  Please ensure all servers  │
│  are started with:          │
│  python launch_all.py       │
│                             │
│      [🔄 Retry Button]      │
│                             │
└─────────────────────────────┘
```

---

## 🖼️ Testing Models

### Upload Image Testing

1. Click a model's **MODEL TESTING** button
2. Wait for loading animation
3. Gradio interface appears with 2 tabs:
   - **📷 Upload Image**
   - **📹 Live Camera**

4. In Upload Image tab:
   - Click or drag image
   - Model processes automatically
   - Results show with bounding boxes

### Live Camera Testing

1. Click **Live Camera** tab
2. Click **Start Camera** button
3. Allow browser camera access
4. Real-time detection appears
5. Click **Stop Camera** when done

---

## 📊 Test Images Included

Sample images in `Testing_images/`:

### LTV/HTV Images (6 images)
- Cars, trucks, buses
- Single and multiple vehicles
- Various angles and distances

### Pedestrian Images (6 images)
- People walking
- Different poses
- Various scenarios

### Traffic Light Images (7 images)
- Red lights
- Yellow lights
- Green lights
- Different conditions

### Traffic Sign Images (7 images)
- Speed limits
- Stop signs
- Directional signs
- Turkish traffic signs

**To use**: Just upload from `Testing_images/` folder!

---

## 🎯 Model Details & Capabilities

### 1. LTV/HTV Detection Model
**What it detects:**
- Light Traffic Vehicles (Cars, motorcycles)
- Heavy Traffic Vehicles (Trucks, buses)

**Best for:**
- Vehicle counting
- Traffic flow analysis
- Parking lot monitoring

**Confidence Threshold:**
- Static images: 40%
- Live camera: 70%

### 2. Pedestrian Detection Model
**What it detects:**
- Pedestrians
- Walking people
- Standing people

**Best for:**
- Crosswalk safety
- Crowd monitoring
- Person counting

**Confidence Threshold:**
- Static images: 40%
- Live camera: 70%

### 3. Traffic Light Detection Model
**What it detects:**
- Red lights 🔴
- Yellow lights 🟡
- Green lights 🟢

**Best for:**
- Autonomous driving
- Traffic signal recognition
- Intersection navigation

**Confidence Threshold:**
- Static images: 50%
- Live camera: 70%

### 4. Traffic Sign Detection Model
**What it detects:**
- 33+ traffic sign types
- Speed limits (20, 30, etc.)
- Directional signs
- Warning signs
- Prohibitory signs

**Special feature**: Turkish to English translation

**Best for:**
- Sign recognition
- Navigation assistance
- Driver assistance systems

**Confidence Threshold:**
- Static images: 40%
- Live camera: 70%

### 5. Autopilot Pro (Combined)
**What it does:**
- Runs ALL 4 models simultaneously
- Complete scene understanding
- Multiple detections in one view

**Best for:**
- Complete autonomous driving
- Full scene analysis
- Testing all capabilities

---

## 🛑 Stopping the System

### Method 1: Terminal (Recommended)
Press `Ctrl+C` in the terminal where `launch_all.py` is running

**You'll see:**
```
⚠️  Interrupt received...

🛑 Shutting down all servers...
  ✓ Server stopped gracefully
  ✓ Server stopped gracefully
  ✓ Server stopped gracefully
  ✓ Server stopped gracefully
  ✓ Server stopped gracefully

✅ All servers stopped. Goodbye! 👋
```

### Method 2: Close Terminal
Simply close the terminal window (all processes will stop)

### Method 3: Manual (If needed)
Kill individual processes:
```bash
# Find process
lsof -ti:7860  # Replace with port number

# Kill it
kill -9 <PID>
```

---

## ❓ Common Questions

### Q: How long does startup take?
**A**: ~60 seconds for all models to load into memory

### Q: Can I use just one model?
**A**: Yes! Run the individual model file:
```bash
cd LTV_HTV_Model
python LTV_HTV_Model.py
```

### Q: Do I need a webcam?
**A**: No, webcam is optional. You can test with uploaded images.

### Q: What if a port is already in use?
**A**: 
```bash
# Kill the process using that port
lsof -ti:7860 | xargs kill -9
```
Or restart your computer.

### Q: Can I change the ports?
**A**: Yes! Edit `config.py`:
```python
SERVER_CONFIG = {
    "LTV_HTV": {
        "port": 7860,  # Change this
        ...
    }
}
```

### Q: Why is the loading animation showing for so long?
**A**: First time loading is slower as models load into RAM. Subsequent uses are faster.

### Q: What if I see "Connection Issue"?
**A**: The server isn't running. Run `python launch_all.py` first.

### Q: Can I run this on a remote server?
**A**: Yes! Change `share=True` in the model files to get public URLs.

---

## 🔧 Customization

### Change Confidence Thresholds

Edit individual model files:
```python
# In predict function
if confidence < 0.4:  # Change this value
    continue
```

Lower = More detections (may include false positives)
Higher = Fewer detections (higher accuracy)

### Change UI Colors

Edit `home.html` CSS section:
```css
:root {
    --primary-color: #1ED760;    /* Change this */
    --secondary-color: #0BCA46;  /* Change this */
    --accent-color: #00BFE8;     /* Change this */
}
```

### Change Server Ports

Edit `launch_all.py`:
```python
"port": 7860,  # Change to any available port
```

Also update `home.html`:
```javascript
onclick="loadGradioApp('http://127.0.0.1:7860')"
                                    // Change port here too
```

---

## 💡 Pro Tips

1. **First Launch**: Takes longer (~2 min) as models load. Be patient!

2. **Good Lighting**: For live camera, ensure good lighting for best results

3. **Image Quality**: Higher resolution images = better detection

4. **Multiple Models**: Use Autopilot Pro to see all detections at once

5. **Performance Metrics**: Check MODEL PERFORMANCE tabs to understand model accuracy

6. **Browser Choice**: Works best with Chrome, Firefox, or Edge

7. **GPU Acceleration**: If you have CUDA-capable GPU, models will use it automatically

8. **Memory**: Keep at least 8GB RAM available for smooth operation

---

## 🎓 Learning Resources

**Understand the models:**
1. Check MODEL PERFORMANCE tabs for metrics
2. Try different test images
3. Compare results across models
4. Experiment with camera angles

**Improve results:**
1. Adjust confidence thresholds
2. Use better lighting
3. Keep subjects at optimal distance
4. Use higher resolution images

---

## 📞 Need Help?

1. **Check** `README.md` for detailed documentation
2. **Review** `QUICK_START.md` for fast reference
3. **Read** `CHANGES_SUMMARY.md` for recent improvements
4. **Run** `python test_system.py` to check system health

---

## ✨ Summary

**You have everything you need:**
- ✅ One-command launch
- ✅ Beautiful loading animations
- ✅ 5 powerful AI models
- ✅ Easy-to-use interface
- ✅ Sample test images
- ✅ Complete documentation

**Just run**: `python launch_all.py` and enjoy! 🚀

---

**Made with ❤️ for awesome AI detection!**

