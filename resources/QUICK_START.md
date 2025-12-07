# 🚀 Quick Start Guide - Autopilot Pro

## Installation & Setup (First Time Only)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the Application

### Option 1: Simple Launch Script (Recommended)

**On macOS/Linux:**
```bash
./start.sh
```

**On Windows:**
```cmd
start.bat
```
(Just double-click the file)

### Option 2: Python Command

```bash
python launch_all.py
```

## What Happens When You Launch?

1. ✅ All 5 Gradio servers start automatically
2. ✅ Each model loads its weights
3. ✅ Health checks confirm servers are ready
4. ✅ UI opens in your default browser
5. ✅ Ready to test!

## Using the Interface

### Testing Individual Models

1. **Click a model button** in the left sidebar:
   - 🚙 LTV/HTV Detection
   - 🚶 Pedestrian Detection
   - 🚦 Traffic Light Detection
   - 🚸 Traffic Sign Detection
   - 🤖 Autopilot Pro (All Models)

2. **Upload an image** or **Start Camera**

3. **View results** with bounding boxes and confidence scores

### Sample Images Included

Test images are provided in `Testing_images/`:
- `LTV_HTV_Images/` - Cars, trucks, buses
- `Pedestrian_Images/` - People walking
- `Traffic_light_images/` - Red, yellow, green lights
- `Traffic_Sign_Images/` - Various traffic signs

## Stopping the Application

Press `Ctrl+C` in the terminal running `launch_all.py`

All servers will shut down gracefully.

## Ports Used

- 7860 - LTV/HTV Model
- 7861 - Pedestrian Model
- 7862 - Traffic Light Model
- 7869 - Traffic Sign Model
- 7868 - Autopilot Pro (Combined)

## Troubleshooting

### "Port already in use"
Kill the process using that port or restart your computer.

### "Model not found"
Ensure all `.pt` files are in their respective model directories.

### "Camera not working"
- Allow camera access in your browser
- Close other apps using the camera
- Try Chrome or Firefox

### Servers not starting
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

## Need More Help?

See the full `README.md` for detailed documentation.

---

**That's it! You're ready to go! 🎉**

Run `./start.sh` (Unix) or `start.bat` (Windows) now!

