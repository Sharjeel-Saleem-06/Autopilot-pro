# 🚗 Autopilot Pro — Multi-Model AI Detection System
Made with **YOLO**, **Gradio**, and **Python** for real-time multi-task perception (vehicles, pedestrians, traffic lights, and traffic signs) with a single-click launcher and a polished web UI.

## 📋 Table of Contents
- [Highlights](#highlights)
- [Live Demos](#live-demos)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Models & Weights](#models--weights)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Model Details](#model-details)
- [Troubleshooting](#troubleshooting)
- [Contact](#contact)

## ✨ Highlights
- Multi-model YOLO pipeline: LTV/HTV, Pedestrian, Traffic Light, Traffic Sign, and Combined Autopilot.
- Single launcher spins up all Gradio apps with health checks.
- Modern UI with loaders, responsive layout, and per-model tabs.
- Image upload and live webcam support.
- Centralized weights folder (`models/`) for easy portability/privacy.

## 🌐 Live Demos
- Netlify UI: https://autopilot-pro.netlify.app/
- Portfolio: https://muhammad-sharjeel-portfolio.netlify.app/

## 🛠️ Tech Stack
- Deep Learning: YOLO (Ultralytics)
- Serving/UI: Gradio
- Language: Python 3.8+
- Frontend: Vanilla HTML/CSS/JS (Netlify)

## 📁 Project Structure

```
Autopilot_Pro/
├── launch_all.py                    # 🚀 MAIN LAUNCHER - Run this file!
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
│
├── AUTOPILOT PRO/                   # Combined model (all detections)
│   └── Autopilotpro.py             # Port 7868
│
├── LTV_HTV_Model/                   # Light/Heavy vehicle detection
│   └── LTV_HTV_Model.py            # Port 7860
│
├── Pedestrian_Model/                # Pedestrian detection
│   └── Pedestrian_Model.py         # Port 7861
│
├── Traffic_Light_Model/             # Traffic light detection
│   └── TRAFFIC_LIGHT_MODEL.py      # Port 7862
│
├── TRAFFIC_SIGN_MODEL/              # Traffic sign detection
│   └── TRAFFIC_SIGN_MODEL.py       # Port 7869
│
├── models/                          # Centralized model weights (portable)
│   ├── ltv_htv.pt
│   ├── pedestrian_last.pt
│   ├── traffic_light_epoch70.pt
│   ├── traffic_sign_trafic.pt
│   └── best_93.pt
│
├── UI/                              # Web interface
│   ├── home.html                   # Main UI
│   ├── home.css                    # Styles
│   └── images/                     # Performance charts & assets
│
└── Testing_images/                  # Sample test images
    ├── LTV_HTV_Images/
    ├── Pedestrian_Images/
    ├── Traffic_light_images/
    └── Traffic_Sign_Images/
```

## 🔧 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Webcam (optional, for live detection)

### Step 1: Clone or Download the Project

```bash
cd /path/to/Autopilot_Pro
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: The installation may take several minutes as it includes PyTorch and other ML libraries.

### Step 3: Verify Model Files (centralized)
Ensure all weights are present in `models/`:
- `ltv_htv.pt`
- `pedestrian_last.pt`
- `traffic_light_epoch70.pt`
- `traffic_sign_trafic.pt`
- `best_93.pt` (additional traffic-sign weight)

## 🚀 Quick Start

### The Easy Way (Recommended)

Run the unified launcher - it automatically starts all models:

```bash
python launch_all.py
```

That's it! The launcher will:

1. ✅ Start all 5 Gradio servers on their respective ports
2. ✅ Wait for each server to be ready
3. ✅ Automatically open the UI in your browser
4. ✅ Show you the status of all servers

### Manual Way (Old Method)

If you prefer to run models individually:

```bash
# Terminal 1 - LTV/HTV Model
python LTV_HTV_Model/LTV_HTV_Model.py

# Terminal 2 - Pedestrian Model
python Pedestrian_Model/Pedestrian_Model.py

# Terminal 3 - Traffic Light Model
python Traffic_Light_Model/TRAFFIC_LIGHT_MODEL.py

# Terminal 4 - Traffic Sign Model
python TRAFFIC_SIGN_MODEL/TRAFFIC_SIGN_MODEL.py

# Terminal 5 - Combined Autopilot
python "AUTOPILOT PRO/Autopilotpro.py"
```

Then open `UI/home.html` in your browser.

## 🎯 Model Details

### 1. LTV/HTV Detection Model

- **Port**: 7860
- **Purpose**: Detects light and heavy traffic vehicles
- **Classes**: Cars, Trucks, Buses, Motorcycles
- **Confidence Threshold**: 0.4 (static), 0.7 (live)

### 2. Pedestrian Detection Model

- **Port**: 7861
- **Purpose**: Identifies pedestrians in the scene
- **Classes**: Pedestrian
- **Confidence Threshold**: 0.4 (static), 0.7 (live)

### 3. Traffic Light Detection Model

- **Port**: 7862
- **Purpose**: Recognizes traffic light states
- **Classes**: Red Light, Yellow Light, Green Light
- **Confidence Threshold**: 0.5 (static), 0.7 (live)

### 4. Traffic Sign Detection Model

- **Port**: 7869
- **Purpose**: Classifies various traffic signs
- **Classes**: 33+ traffic sign types
- **Features**: Turkish to English translation
- **Confidence Threshold**: 0.4 (static), 0.7 (live)

### 5. Autopilot Pro (Combined)

- **Port**: 7868
- **Purpose**: Runs all models simultaneously
- **Use Case**: Complete scene understanding

## 💻 Usage

### Using the Web Interface

1. **Start the system**:

   ```bash
   python launch_all.py
   ```
2. **Navigate the UI**:

   - The UI opens automatically at `UI/home.html`
   - Use the left sidebar to select different models
   - Click "MODEL TESTING" buttons to test individual models
   - View performance metrics in the tabs
3. **Test with Images**:

   - Click "Upload Image" tab
   - Upload an image from `Testing_images/`
   - View detection results with bounding boxes
4. **Live Camera Detection**:

   - Click "Live Camera" tab
   - Click "Start Camera" button
   - Allow browser to access your webcam
   - View real-time detections

### Testing with Sample Images

The project includes test images in `Testing_images/`:

```
Testing_images/
├── LTV_HTV_Images/      # Vehicle test images
├── Pedestrian_Images/   # Pedestrian test images
├── Traffic_light_images/# Traffic light test images
└── Traffic_Sign_Images/ # Traffic sign test images
```

### Stopping the System

Press `Ctrl+C` in the terminal where `launch_all.py` is running. This will gracefully shut down all servers.

## 🔍 Server Ports

| Service                | Port | URL                   |
| ---------------------- | ---- | --------------------- |
| LTV/HTV Model          | 7860 | http://127.0.0.1:7860 |
| Pedestrian Model       | 7861 | http://127.0.0.1:7861 |
| Traffic Light Model    | 7862 | http://127.0.0.1:7862 |
| Traffic Sign Model     | 7869 | http://127.0.0.1:7869 |
| Autopilot Pro Combined | 7868 | http://127.0.0.1:7868 |

## 🛠️ Troubleshooting

### Issue: "Port already in use"

**Solution**:

```bash
# Kill processes on specific port (example for port 7860)
# On macOS/Linux:
lsof -ti:7860 | xargs kill -9

# On Windows:
netstat -ano | findstr :7860
taskkill /PID <PID> /F
```

Or simply restart your computer.

### Issue: "Model file not found"

**Solution**: Ensure all `.pt` model files are present in the `models/` folder. Re-download if necessary.

### Issue: "Camera not working"

**Solutions**:

- Grant camera permissions in browser
- Check if another application is using the camera
- Try a different browser (Chrome/Firefox recommended)

### Issue: Gradio server not starting

**Solutions**:

```bash
# Upgrade gradio
pip install --upgrade gradio

# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: Low detection accuracy

**Solutions**:

- Ensure good lighting conditions
- Keep objects at appropriate distance
- Use higher resolution images
- Adjust confidence thresholds in the model files

### Issue: High memory usage

**Solution**: Close other applications. YOLO models require significant RAM (8GB+ recommended).

## 🔧 Advanced Configuration

### Changing Confidence Thresholds

Edit the model files to adjust confidence thresholds:

```python
# In each model file, find:
if confidence < 0.4:  # Change this value (0.0 to 1.0)
    continue
```

Lower values = more detections (may include false positives)
Higher values = fewer detections (higher accuracy)

### Changing Server Ports

Edit `launch_all.py` and modify the `servers` list:

```python
{
    "name": "LTV/HTV Detection",
    "script": ...,
    "port": 7860,  # Change this
    ...
}
```

Don't forget to update `UI/home.html` accordingly:

```javascript
<button onclick="loadGradioApp('http://127.0.0.1:7860')">
```

## 📊 Performance Metrics

View detailed performance metrics in the UI:

- **Training Loss**: Model training convergence
- **Precision**: Accuracy of positive predictions
- **Recall**: Coverage of actual positives
- **mAP (Mean Average Precision)**: Overall detection accuracy
- **Confusion Matrix**: Class-wise performance

## 📝 Notes
- GPU acceleration: auto-uses CUDA if available.
- Model size: total weights ~500MB+ (kept in `models/`).
- Browser compatibility: Chrome/Firefox/Edge recommended.

## 📞 Contact
- Email: sharry00010@gmail.com
- Portfolio: https://muhammad-sharjeel-portfolio.netlify.app/

---
**Made with YOLO, Gradio, and Python**  
🚀 **Ready to test? Run `python launch_all.py` now!**
