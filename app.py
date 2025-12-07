#!/usr/bin/env python3
"""
Autopilot Pro - Unified Deployment App
=======================================
Single Gradio app with all 5 models in tabs for easy deployment
Perfect for Hugging Face Spaces, Railway, Render, etc.
"""

import gradio as gr
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO
import os
from pathlib import Path

# ============================================================================
# MODEL LOADING
# ============================================================================

print("🚀 Loading Autopilot Pro models...")

base_dir = Path(__file__).parent

# Model paths
MODEL_PATHS = {
    "LTV_HTV": base_dir / "LTV_HTV_Model" / "LTV_HTV.pt",
    "Pedestrian": base_dir / "Pedestrian_Model" / "last.pt",
    "TrafficLight": base_dir / "Traffic_Light_Model" / "epoch70.pt",
    "TrafficSign": base_dir / "TRAFFIC_SIGN_MODEL" / "trafic.pt",
}

# Load all models
models = {}
for name, path in MODEL_PATHS.items():
    if path.exists():
        try:
            models[name] = YOLO(str(path))
            print(f"✅ {name} model loaded")
        except Exception as e:
            print(f"❌ Error loading {name}: {e}")
            models[name] = None
    else:
        print(f"⚠️  {name} model not found at {path}")
        models[name] = None

# Traffic sign translations
TRAFFIC_SIGN_TRANSLATIONS = {
    "20": "Speed Limit 20", "30": "Speed Limit 30",
    "dur": "Stop", "durak": "Bus Stop",
    "girisyok": "No Entry", "ilerisag": "Go Straight & Turn Right",
    "ilerisol": "Go Straight & Turn Left", "kirmizi": "Red Light",
    "park": "Parking", "parkyasak": "No Parking",
    "sag": "Right", "sagadonulmez": "No Right Turn",
    "sari": "Yellow Light", "sol": "Left",
    "soladonulmez": "No Left Turn", "yesil": "Green Light",
    "parkyasak2": "No Parking (Variant)", "arac": "Vehicle",
    "yaya": "Pedestrian", "otobus": "Bus",
    "bisikletli": "Cyclist", "yapılar": "Buildings",
    "yayagecidi": "Pedestrian Crossing", "tasitrafiginekapali": "Closed to Vehicle Traffic"
}

# ============================================================================
# INFERENCE FUNCTIONS
# ============================================================================

def run_inference(image, model_name, confidence_threshold=0.4, color=(0, 255, 0)):
    """Generic inference function for any model"""
    if models.get(model_name) is None:
        return image, "❌ Model not loaded"
    
    try:
        img_array = np.array(image.convert('RGB'))
        results = models[model_name](img_array)
        
        detected_count = 0
        detection_info = []
        
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0]) if box.conf is not None else 0
                cls_index = int(box.cls[0]) if box.cls is not None else -1
                
                if confidence < confidence_threshold or cls_index == -1:
                    continue
                
                # Get label
                label = models[model_name].names[cls_index] if hasattr(models[model_name], "names") and cls_index in models[model_name].names else f"Class_{cls_index}"
                
                # Translate traffic signs
                if model_name == "TrafficSign":
                    label = TRAFFIC_SIGN_TRANSLATIONS.get(label, label)
                
                detected_count += 1
                detection_info.append(f"{label}: {confidence:.2f}")
                
                # Draw bounding box
                cv2.rectangle(img_array, (x1, y1), (x2, y2), color, 3)
                cv2.putText(img_array, f"{label} {confidence:.2f}", (x1, y1 - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA)
        
        result_image = Image.fromarray(img_array)
        info_text = f"✅ Detected {detected_count} objects\n" + "\n".join(detection_info[:10])
        if len(detection_info) > 10:
            info_text += f"\n... and {len(detection_info) - 10} more"
        
        return result_image, info_text if detected_count > 0 else "No objects detected"
    
    except Exception as e:
        return image, f"❌ Error: {str(e)}"

def run_combined_inference(image, confidence_threshold=0.4):
    """Run all models on the same image"""
    if not any(models.values()):
        return image, "❌ No models loaded"
    
    try:
        img_array = np.array(image.convert('RGB'))
        total_detections = 0
        detection_summary = {}
        
        colors = {
            "LTV_HTV": (0, 255, 0),      # Green
            "Pedestrian": (255, 0, 0),   # Red
            "TrafficLight": (0, 165, 255),  # Orange
            "TrafficSign": (255, 0, 255)  # Magenta
        }
        
        for model_name, model in models.items():
            if model is None:
                continue
            
            results = model(img_array)
            model_detections = []
            
            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    confidence = float(box.conf[0]) if box.conf is not None else 0
                    cls_index = int(box.cls[0]) if box.cls is not None else -1
                    
                    if confidence < confidence_threshold or cls_index == -1:
                        continue
                    
                    label = model.names[cls_index] if hasattr(model, "names") and cls_index in model.names else f"Class_{cls_index}"
                    
                    if model_name == "TrafficSign":
                        label = TRAFFIC_SIGN_TRANSLATIONS.get(label, label)
                    
                    total_detections += 1
                    model_detections.append(label)
                    
                    # Draw with model-specific color
                    color = colors.get(model_name, (0, 255, 0))
                    cv2.rectangle(img_array, (x1, y1), (x2, y2), color, 3)
                    cv2.putText(img_array, f"{label} {confidence:.2f}", (x1, y1 - 10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA)
            
            if model_detections:
                detection_summary[model_name] = len(model_detections)
        
        result_image = Image.fromarray(img_array)
        
        summary_text = f"✅ Total Detections: {total_detections}\n\n"
        for model_name, count in detection_summary.items():
            icon = {"LTV_HTV": "🚙", "Pedestrian": "🚶", "TrafficLight": "🚦", "TrafficSign": "🚸"}.get(model_name, "📦")
            summary_text += f"{icon} {model_name}: {count}\n"
        
        return result_image, summary_text if total_detections > 0 else "No objects detected"
    
    except Exception as e:
        return image, f"❌ Error: {str(e)}"

# ============================================================================
# INDIVIDUAL MODEL INTERFACES
# ============================================================================

def ltv_htv_detect(image, confidence):
    return run_inference(image, "LTV_HTV", confidence, (0, 255, 0))

def pedestrian_detect(image, confidence):
    return run_inference(image, "Pedestrian", confidence, (255, 0, 0))

def traffic_light_detect(image, confidence):
    return run_inference(image, "TrafficLight", confidence, (0, 165, 255))

def traffic_sign_detect(image, confidence):
    return run_inference(image, "TrafficSign", confidence, (255, 0, 255))

def combined_detect(image, confidence):
    return run_combined_inference(image, confidence)

# ============================================================================
# GRADIO INTERFACE
# ============================================================================

# Custom CSS for better appearance - Professional & Clean Design
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ============================================
   GLOBAL STYLES - Clean Professional Theme
   ============================================ */

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

/* Main Container - Pure White Background */
.gradio-container {
    background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%) !important;
    max-width: 100% !important;
    padding: 0 !important;
}

body {
    background: #ffffff !important;
    color: #1a1a1a !important;
}

.gradio-container,
.gradio-container * {
    color: #1a1a1a !important;
}

.gradio-container p,
.gradio-container label,
.gradio-container span,
.gradio-container strong,
.gradio-container h1,
.gradio-container h2,
.gradio-container h3,
.gradio-container h4,
.gradio-container h5,
.gradio-container h6,
.gradio-container .prose * {
    color: #1a1a1a !important;
}

/* Make dark badges legible */
.gradio-container .label,
.gradio-container .label * {
    background: transparent !important;
    color: #1a1a1a !important;
    border: none !important;
    box-shadow: none !important;
}

/* Extra safety: label wrappers */
.gradio-container .label-wrap,
.gradio-container .label-wrap *,
.gradio-container .block .label,
.gradio-container .block .label * {
    background: transparent !important;
    color: #1a1a1a !important;
    border: none !important;
    box-shadow: none !important;
}

/* Kill any remaining dark label badges (inputs/outputs) */
.gradio-container .label:before,
.gradio-container .label:after,
.gradio-container .input-image .label,
.gradio-container .output-image .label,
.gradio-container .image .label,
.gradio-container [class*="label"]:not(button) {
    background: transparent !important;
    color: #1a1a1a !important;
    border: none !important;
    box-shadow: none !important;
}

/* Extra force: all label elements and spans */
.gradio-container label,
.gradio-container label *,
.gradio-container .block label,
.gradio-container .block label *,
.gradio-container [class*="label"],
.gradio-container [class*="label"] * {
    background: transparent !important;
    background-color: transparent !important;
    color: #1a1a1a !important;
    border: none !important;
    box-shadow: none !important;
    mix-blend-mode: normal !important;
}

/* Flatten corners on image input/output containers */
.gradio-container .gr-image,
.gradio-container .image-container,
.gradio-container .input-image,
.gradio-container .output-image,
.gradio-container .image {
    border-radius: 0 !important;
}

/* Camera/Webcam & image toolbars: light buttons, no black pills */
.gradio-container .image-container button,
.gradio-container .image-container .toolbar button,
.gradio-container .image-container .controls button,
.gradio-container .image-container .absolute button,
.gradio-container .image-container [class*="tool"] button,
.gradio-container .image-container [class*="control"] button {
    background: rgba(255, 255, 255, 0.92) !important;
    color: #1a1a1a !important;
    border: 1px solid #e5e7eb !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08) !important;
    border-radius: 8px !important;
}

.gradio-container .image-container button:hover,
.gradio-container .image-container .toolbar button:hover,
.gradio-container .image-container .controls button:hover,
.gradio-container .image-container .absolute button:hover {
    background: #ffffff !important;
    border-color: #d1d5db !important;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.12) !important;
}

.gradio-container .image-container button svg,
.gradio-container .image-container button svg path,
.gradio-container .image-container button svg rect,
.gradio-container .image-container button svg circle {
    fill: #1a1a1a !important;
    stroke: #1a1a1a !important;
}

/* Webcam source dropdowns and camera overlay controls */
.gradio-container .image-container select,
.gradio-container .image-container .dropdown,
.gradio-container .image-container .dropdown * {
    background: rgba(255, 255, 255, 0.96) !important;
    color: #111827 !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 10px !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08) !important;
}

.gradio-container .image-container [class*="camera"],
.gradio-container .image-container [class*="webcam"],
.gradio-container .image-container [class*="cam"],
.gradio-container .image-container [class*="dropdown"],
.gradio-container .image-container [class*="video"],
.gradio-container .image-container [class*="control"],
.gradio-container .image-container [class*="options"] {
    background: rgba(255, 255, 255, 0.96) !important;
    color: #111827 !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 10px !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08) !important;
}

.gradio-container .image-container [class*="camera"] svg,
.gradio-container .image-container [class*="webcam"] svg,
.gradio-container .image-container [class*="cam"] svg,
.gradio-container .image-container [class*="dropdown"] svg,
.gradio-container .image-container [class*="video"] svg {
    fill: #111827 !important;
    stroke: #111827 !important;
}

.contain, .wrap {
    background: transparent !important;
}

.main {
    background: transparent !important;
    padding: 30px 40px !important;
}

/* ============================================
   TABS - Modern Professional Design
   ============================================ */

.tabs {
    border-radius: 16px !important;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08) !important;
    background: #ffffff !important;
    border: 1px solid #e8e8e8 !important;
}

.tab-nav {
    background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%) !important;
    padding: 16px 20px !important;
    border-bottom: 2px solid #e8e8e8 !important;
    display: flex;
    gap: 10px !important;
}

.tab-nav button {
    color: #4a5568 !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    border-radius: 12px !important;
    padding: 14px 28px !important;
    background: #ffffff !important;
    border: 2px solid #e2e8f0 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
}

.tab-nav button:hover {
    background: linear-gradient(135deg, #f0f4ff 0%, #e8f0ff 100%) !important;
    color: #2563eb !important;
    transform: translateY(-2px);
    border-color: #2563eb !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15) !important;
}

.tab-nav button.selected {
    background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%) !important;
    color: #ffffff !important;
    box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4) !important;
    border-color: #1e40af !important;
    font-weight: 700 !important;
}

/* ============================================
   BUTTONS - Vibrant & Professional
   ============================================ */

.gr-button {
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    padding: 14px 32px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    border: none !important;
    cursor: pointer !important;
}

.gr-button-primary {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    color: white !important;
    box-shadow: 0 6px 24px rgba(16, 185, 129, 0.35) !important;
}

.gr-button-primary:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 32px rgba(16, 185, 129, 0.5) !important;
    background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
}

.gr-button-primary:active {
    transform: translateY(-1px) !important;
}

/* ============================================
   INPUT/OUTPUT AREAS - Clean Cards (No Dark Panels)
   ============================================ */

.gr-group {
    background: #ffffff !important;
    border: 1px solid #e8e8e8 !important;
    border-radius: 16px !important;
    padding: 28px !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06) !important;
    transition: all 0.3s ease !important;
    color: #1a1a1a !important;
}

.gr-group:hover {
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1) !important;
    border-color: #2563eb !important;
}

.gr-box,
.gr-panel,
.panel,
.gr-accordion,
.gr-accordion > div {
    border-radius: 12px !important;
    border: 2px solid #e8e8e8 !important;
    background: #ffffff !important;
    transition: all 0.3s ease !important;
    color: #1a1a1a !important;
}

.gr-box:hover,
.gr-panel:hover,
.panel:hover,
.gr-accordion:hover {
    border-color: #2563eb !important;
}

/* Force all default Gradio blocks to stay light */
.gradio-container .block,
.gradio-container .form,
.gradio-container .tabs,
.gradio-container .tabitem {
    background: #ffffff !important;
    color: #1a1a1a !important;
}

/* ============================================
   IMAGE UPLOAD - Modern Drag & Drop
   ============================================ */

.gr-image {
    border-radius: 12px !important;
    overflow: hidden !important;
    background: #ffffff !important;
    border: 2px solid #e8e8e8 !important;
}

.gr-file-upload {
    background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%) !important;
    border: 3px dashed #cbd5e0 !important;
    border-radius: 16px !important;
    padding: 48px 32px !important;
    text-align: center !important;
    transition: all 0.3s ease !important;
    cursor: pointer !important;
}

.gr-file-upload:hover {
    background: linear-gradient(135deg, #e8f0ff 0%, #f0f8ff 100%) !important;
    border-color: #2563eb !important;
    border-width: 3px !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(37, 99, 235, 0.15) !important;
}

.image-container {
    background: #ffffff !important;
    border: 2px solid #e8e8e8 !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

.gr-image img {
    border-radius: 8px !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08) !important;
}

/* ============================================
   ACCORDION - Clean Expandable Sections
   ============================================ */

.gr-accordion {
    background: #f8f9fa !important;
    border: 1px solid #e8e8e8 !important;
    border-radius: 12px !important;
    margin-top: 16px !important;
    overflow: hidden !important;
}

.gr-accordion summary {
    font-weight: 600 !important;
    color: #1a1a1a !important;
    padding: 16px 20px !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
}

.gr-accordion summary:hover {
    background: #e8f0ff !important;
    color: #2563eb !important;
}

/* ============================================
   FORM CONTROLS - Modern Inputs
   ============================================ */

.gr-form label {
    font-weight: 600 !important;
    color: #1a1a1a !important;
    font-size: 14px !important;
    letter-spacing: 0.3px !important;
    margin-bottom: 8px !important;
    display: block !important;
}

/* Slider */
.gr-slider {
    padding: 16px 0 !important;
}

.gr-slider input[type="range"] {
    -webkit-appearance: none !important;
    appearance: none !important;
    height: 8px !important;
    border-radius: 5px !important;
    background: linear-gradient(90deg, #2563eb 0%, #1e40af 100%) !important;
    outline: none !important;
}

.gr-slider input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none !important;
    appearance: none !important;
    width: 20px !important;
    height: 20px !important;
    border-radius: 50% !important;
    background: #ffffff !important;
    cursor: pointer !important;
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.4) !important;
    border: 3px solid #2563eb !important;
}

.gr-slider input[type="range"]::-moz-range-thumb {
    width: 20px !important;
    height: 20px !important;
    border-radius: 50% !important;
    background: #ffffff !important;
    cursor: pointer !important;
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.4) !important;
    border: 3px solid #2563eb !important;
}

/* Textbox & Textarea */
.gr-textbox, textarea, input[type="text"], input[type="number"] {
    border-radius: 10px !important;
    border: 2px solid #e8e8e8 !important;
    padding: 14px 16px !important;
    background: #ffffff !important;
    color: #1a1a1a !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
    transition: all 0.3s ease !important;
    text-align: center !important;
    box-shadow: none !important;
    outline: none !important;
    appearance: none !important;
    -webkit-appearance: none !important;
}

.gr-textbox:focus, textarea:focus, input:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1) !important;
    outline: none !important;
    background: #ffffff !important;
}

/* Remove number input spin buttons */
input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

input[type="number"] {
    -moz-appearance: textfield;
}

/* Hide appended random/reset button on number inputs (keep value only) */
.gradio-container .gr-slider input[type="number"] + button,
.gradio-container .number input + button,
.gradio-container .input-number input + button {
    display: none !important;
}

/* Force-hide any residual buttons/icons next to numeric inputs */
.gradio-container .gr-number button,
.gradio-container .gr-number button *,
.gradio-container .gr-slider button,
.gradio-container .slider-container button,
.gradio-container .number button,
.gradio-container .input-number button {
    display: none !important;
    visibility: hidden !important;
    width: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    border: none !important;
}

/* Flatten slider number box styling */
.gradio-container .gr-slider input[type="number"] {
    border: 1px solid #d1d5db !important;
    border-radius: 8px !important;
    box-shadow: none !important;
    background: #fff !important;
    padding: 10px 12px !important;
    height: 38px !important;
    line-height: 1.4 !important;
    text-align: center !important;
}

.gradio-container .gr-slider input[type="number"]:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.15) !important;
    outline: none !important;
}

/* ============================================
   TYPOGRAPHY - Clear & Readable
   ============================================ */

h1, h2, h3, h4, h5, h6 {
    color: #1a1a1a !important;
    font-weight: 700 !important;
    line-height: 1.3 !important;
}

h2 {
    font-size: 28px !important;
    margin-bottom: 8px !important;
}

h3 {
    font-size: 18px !important;
    margin-bottom: 16px !important;
    color: #2d3748 !important;
}

p {
    color: #4a5568 !important;
    line-height: 1.7 !important;
    font-size: 15px !important;
}

/* ============================================
   SPACING & LAYOUT
   ============================================ */

.gr-row {
    gap: 24px !important;
    margin-bottom: 16px !important;
}

.gr-column {
    gap: 20px !important;
}

.tabitem {
    padding: 32px !important;
    background: transparent !important;
}

/* ============================================
   FOOTER & BRANDING
   ============================================ */

footer {
    display: none !important;
}

.gradio-container .footer {
    display: none !important;
}

/* ============================================
   ANIMATIONS
   ============================================ */

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes pulse {
    0%, 100% {
        opacity: 1;
    }
    50% {
        opacity: 0.8;
    }
}

.gr-group, .gr-box {
    animation: fadeInUp 0.5s ease-out;
}

/* ============================================
   RESPONSIVE DESIGN
   ============================================ */

@media (max-width: 1024px) {
    .main {
        padding: 20px !important;
    }
    
    .tab-nav button {
        padding: 12px 20px !important;
        font-size: 14px !important;
    }
}

@media (max-width: 768px) {
    .main {
        padding: 16px !important;
    }
    
    .gr-button-primary {
        width: 100% !important;
        padding: 16px !important;
    }
    
    .tab-nav {
        flex-wrap: wrap !important;
    }
    
    .tab-nav button {
        flex: 1 1 auto !important;
        min-width: 140px !important;
    }
    
    .gr-group {
        padding: 20px !important;
    }
    
    h2 {
        font-size: 24px !important;
    }
}

@media (max-width: 480px) {
    .main {
        padding: 12px !important;
    }
    
    .tabitem {
        padding: 16px !important;
    }
    
    .tab-nav button {
        font-size: 13px !important;
        padding: 10px 16px !important;
    }
}

/* ============================================
   CUSTOM INFO BOXES
   ============================================ */

.info-box {
    background: linear-gradient(135deg, #e8f4fd 0%, #d4e9fc 100%);
    border-left: 4px solid #2563eb;
    padding: 16px 20px;
    border-radius: 8px;
    margin: 12px 0;
}

.warning-box {
    background: linear-gradient(135deg, #fff9e6 0%, #fef3c7 100%);
    border-left: 4px solid #f59e0b;
    padding: 16px 20px;
    border-radius: 8px;
    margin: 12px 0;
}

.success-box {
    background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
    border-left: 4px solid #10b981;
    padding: 16px 20px;
    border-radius: 8px;
    margin: 12px 0;
}

/* ============================================
   LOADING STATES
   ============================================ */

.gr-loading {
    animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* ============================================
   SCROLLBAR STYLING
   ============================================ */

::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
}
"""

# Create the interface
with gr.Blocks(css=custom_css, title="🚗 Autopilot Pro - AI Detection System") as demo:
    
    with gr.Tabs():
        
        # Tab 1: LTV/HTV Detection
        with gr.Tab("🚙 LTV/HTV Detection"):
            with gr.Row():
                gr.Markdown("""
                <div style='text-align: center; padding: 32px; background: linear-gradient(135deg, #e0f2fe 0%, #e8f4fd 100%); border: 2px solid #0ea5e9; border-radius: 20px; margin-bottom: 28px; box-shadow: 0 8px 24px rgba(14, 165, 233, 0.15);'>
                    <h2 style='margin: 0; font-size: 32px; color: #0c4a6e; font-weight: 800; letter-spacing: -0.5px;'>🚙 Light & Heavy Traffic Vehicle Detection</h2>
                    <p style='margin: 16px 0 0 0; color: #0369a1; font-size: 16px; font-weight: 500;'>AI-powered vehicle classification for intelligent traffic monitoring</p>
                </div>
                """)
            
            with gr.Row():
                # Left Panel - Input Controls
                with gr.Column(scale=1):
                    with gr.Group():
                        gr.Markdown("### 📤 Upload & Configure")
                        ltv_input = gr.Image(
                            type="pil", 
                            label="Image Input",
                            height=300
                        )
                        
                        with gr.Accordion("⚙️ Detection Settings", open=True):
                            ltv_confidence = gr.Slider(
                                0.1, 1.0, 
                                value=0.4, 
                                label="🎯 Confidence Threshold",
                                info="Higher = More accurate, Lower = More detections"
                            )
                            
                            gr.Markdown("""
                            <div style='background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); padding: 16px; border-radius: 12px; margin-top: 12px; border: 1px solid #bae6fd;'>
                                <strong style='color: #0c4a6e; font-size: 15px;'>💡 Model Info:</strong><br/>
                                <ul style='margin: 10px 0; padding-left: 20px; font-size: 14px; color: #0369a1; line-height: 1.8;'>
                                    <li><strong>Classes:</strong> LTV (Light) & HTV (Heavy)</li>
                                    <li><strong>Accuracy:</strong> 98.3% mAP</li>
                                    <li><strong>Speed:</strong> ~13 FPS</li>
                                </ul>
                            </div>
                            """)
                        
                        ltv_button = gr.Button(
                            "🚀 Detect Vehicles", 
                            variant="primary",
                            size="lg"
                        )
                        
                        gr.Markdown("""
                        <div style='text-align: center; margin-top: 16px; padding: 14px; background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-radius: 10px; font-size: 14px; border: 1px solid #fbbf24; color: #92400e; font-weight: 600;'>
                            💡 <strong>Tip:</strong> Works best with clear road images
                        </div>
                        """)
                
                # Right Panel - Results
                with gr.Column(scale=1):
                    with gr.Group():
                        gr.Markdown("### 📊 Detection Results")
                        ltv_output = gr.Image(
                            type="pil", 
                            label="Detected Vehicles",
                            height=300
                        )
                        
                        with gr.Accordion("📈 Detection Details", open=True):
                            ltv_info = gr.Textbox(
                                label="Analysis Report",
                                lines=8,
                                placeholder="Upload an image to see detection details..."
                            )
            
            ltv_button.click(ltv_htv_detect, inputs=[ltv_input, ltv_confidence], outputs=[ltv_output, ltv_info])
            ltv_input.change(ltv_htv_detect, inputs=[ltv_input, ltv_confidence], outputs=[ltv_output, ltv_info])
        
        # Tab 2: Pedestrian Detection
        with gr.Tab("🚶 Pedestrian Detection"):
            with gr.Row():
                gr.Markdown("""
                <div style='text-align: center; padding: 32px; background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%); border: 2px solid #ef4444; border-radius: 20px; margin-bottom: 28px; box-shadow: 0 8px 24px rgba(239, 68, 68, 0.15);'>
                    <h2 style='margin: 0; font-size: 32px; color: #991b1b; font-weight: 800; letter-spacing: -0.5px;'>🚶 Pedestrian Detection System</h2>
                    <p style='margin: 16px 0 0 0; color: #dc2626; font-size: 16px; font-weight: 500;'>Advanced pedestrian detection for crosswalk safety & monitoring</p>
                </div>
                """)
            
            with gr.Row():
                with gr.Column(scale=1):
                    with gr.Group():
                        gr.Markdown("### 📤 Upload & Configure")
                        ped_input = gr.Image(type="pil", label="Image Input", height=300)
                        
                        with gr.Accordion("⚙️ Detection Settings", open=True):
                            ped_confidence = gr.Slider(
                                0.1, 1.0, value=0.4, 
                                label="🎯 Confidence Threshold",
                                info="Adjust sensitivity for pedestrian detection"
                            )
                            
                            gr.Markdown("""
                            <div style='background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%); padding: 16px; border-radius: 12px; margin-top: 12px; border: 1px solid #fecaca;'>
                                <strong style='color: #991b1b; font-size: 15px;'>💡 Model Info:</strong><br/>
                                <ul style='margin: 10px 0; padding-left: 20px; font-size: 14px; color: #7f1d1d; line-height: 1.8;'>
                                    <li><strong>Classes:</strong> Pedestrians</li>
                                    <li><strong>Accuracy:</strong> 85.7% mAP</li>
                                    <li><strong>Dataset:</strong> 18,000+ images</li>
                                </ul>
                            </div>
                            """)
                        
                        ped_button = gr.Button("🚀 Detect Pedestrians", variant="primary", size="lg")
                        
                        gr.Markdown("""
                        <div style='text-align: center; margin-top: 16px; padding: 14px; background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); border-radius: 10px; font-size: 14px; border: 1px solid #ef4444; color: #991b1b; font-weight: 600;'>
                            💡 <strong>Tip:</strong> Best for crosswalk and street scenes
                        </div>
                        """)
                
                with gr.Column(scale=1):
                    with gr.Group():
                        gr.Markdown("### 📊 Detection Results")
                        ped_output = gr.Image(type="pil", label="Detected Pedestrians", height=300)
                        
                        with gr.Accordion("📈 Detection Details", open=True):
                            ped_info = gr.Textbox(
                                label="Analysis Report", 
                                lines=8,
                                placeholder="Upload an image to see detection details..."
                            )
            
            ped_button.click(pedestrian_detect, inputs=[ped_input, ped_confidence], outputs=[ped_output, ped_info])
            ped_input.change(pedestrian_detect, inputs=[ped_input, ped_confidence], outputs=[ped_output, ped_info])
        
        # Tab 3: Traffic Light Detection
        with gr.Tab("🚦 Traffic Light Detection"):
            with gr.Row():
                gr.Markdown("""
                <div style='text-align: center; padding: 32px; background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); border: 2px solid #f59e0b; border-radius: 20px; margin-bottom: 28px; box-shadow: 0 8px 24px rgba(245, 158, 11, 0.15);'>
                    <h2 style='margin: 0; font-size: 32px; color: #92400e; font-weight: 800; letter-spacing: -0.5px;'>🚦 Traffic Light State Detection</h2>
                    <p style='margin: 16px 0 0 0; color: #d97706; font-size: 16px; font-weight: 500;'>Detect Red, Yellow, Green & Off states for intersection navigation</p>
                </div>
                """)
            
            with gr.Row():
                with gr.Column(scale=1):
                    with gr.Group():
                        gr.Markdown("### 📤 Upload & Configure")
                        tl_input = gr.Image(type="pil", label="Image Input", height=300)
                        
                        with gr.Accordion("⚙️ Detection Settings", open=True):
                            tl_confidence = gr.Slider(
                                0.1, 1.0, value=0.5, 
                                label="🎯 Confidence Threshold",
                                info="Higher threshold for traffic light accuracy"
                            )
                            
                            gr.Markdown("""
                            <div style='background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); padding: 16px; border-radius: 12px; margin-top: 12px; border: 1px solid #fde68a;'>
                                <strong style='color: #92400e; font-size: 15px;'>💡 Model Info:</strong><br/>
                                <ul style='margin: 10px 0; padding-left: 20px; font-size: 14px; color: #b45309; line-height: 1.8;'>
                                    <li><strong>States:</strong> 🔴 Red, 🟡 Yellow, 🟢 Green, ⚪ Off</li>
                                    <li><strong>Accuracy:</strong> 100% mAP@50</li>
                                    <li><strong>Dataset:</strong> 6,034 images</li>
                                </ul>
                            </div>
                            """)
                        
                        tl_button = gr.Button("🚀 Detect Traffic Lights", variant="primary", size="lg")
                        
                        gr.Markdown("""
                        <div style='text-align: center; margin-top: 16px; padding: 14px; background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-radius: 10px; font-size: 14px; border: 1px solid #f59e0b; color: #92400e; font-weight: 600;'>
                            💡 <strong>Tip:</strong> Works at intersections and traffic signals
                        </div>
                        """)
                
                with gr.Column(scale=1):
                    with gr.Group():
                        gr.Markdown("### 📊 Detection Results")
                        tl_output = gr.Image(type="pil", label="Detected Traffic Lights", height=300)
                        
                        with gr.Accordion("📈 Detection Details", open=True):
                            tl_info = gr.Textbox(
                                label="Analysis Report", 
                                lines=8,
                                placeholder="Upload an image to see detection details..."
                            )
            
            tl_button.click(traffic_light_detect, inputs=[tl_input, tl_confidence], outputs=[tl_output, tl_info])
            tl_input.change(traffic_light_detect, inputs=[tl_input, tl_confidence], outputs=[tl_output, tl_info])
        
        # Tab 4: Traffic Sign Detection
        with gr.Tab("🚸 Traffic Sign Detection"):
            with gr.Row():
                gr.Markdown("""
                <div style='text-align: center; padding: 32px; background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%); border: 2px solid #a855f7; border-radius: 20px; margin-bottom: 28px; box-shadow: 0 8px 24px rgba(168, 85, 247, 0.15);'>
                    <h2 style='margin: 0; font-size: 32px; color: #6b21a8; font-weight: 800; letter-spacing: -0.5px;'>🚸 Traffic Sign Recognition (33+ Types)</h2>
                    <p style='margin: 16px 0 0 0; color: #9333ea; font-size: 16px; font-weight: 500;'>Comprehensive traffic sign classification for complete road understanding</p>
                </div>
                """)
            
            with gr.Row():
                with gr.Column(scale=1):
                    with gr.Group():
                        gr.Markdown("### 📤 Upload & Configure")
                        ts_input = gr.Image(type="pil", label="Image Input", height=300)
                        
                        with gr.Accordion("⚙️ Detection Settings", open=True):
                            ts_confidence = gr.Slider(
                                0.1, 1.0, value=0.4, 
                                label="🎯 Confidence Threshold",
                                info="Fine-tune sign classification sensitivity"
                            )
                            
                            gr.Markdown("""
                            <div style='background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%); padding: 16px; border-radius: 12px; margin-top: 12px; border: 1px solid #e9d5ff;'>
                                <strong style='color: #6b21a8; font-size: 15px;'>💡 Model Info:</strong><br/>
                                <ul style='margin: 10px 0; padding-left: 20px; font-size: 14px; color: #7c3aed; line-height: 1.8;'>
                                    <li><strong>Signs:</strong> 33+ traffic sign types</li>
                                    <li><strong>Categories:</strong> Warning, regulatory, guide</li>
                                    <li><strong>Speed:</strong> Real-time detection</li>
                                </ul>
                            </div>
                            """)
                        
                        ts_button = gr.Button("🚀 Detect Traffic Signs", variant="primary", size="lg")
                        
                        gr.Markdown("""
                        <div style='text-align: center; margin-top: 16px; padding: 14px; background: linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 100%); border-radius: 10px; font-size: 14px; border: 1px solid #a855f7; color: #6b21a8; font-weight: 600;'>
                            💡 <strong>Tip:</strong> Captures most common road signs
                        </div>
                        """)
                
                with gr.Column(scale=1):
                    with gr.Group():
                        gr.Markdown("### 📊 Detection Results")
                        ts_output = gr.Image(type="pil", label="Detected Traffic Signs", height=300)
                        
                        with gr.Accordion("📈 Detection Details", open=True):
                            ts_info = gr.Textbox(
                                label="Analysis Report", 
                                lines=8,
                                placeholder="Upload an image to see detection details..."
                            )
            
            ts_button.click(traffic_sign_detect, inputs=[ts_input, ts_confidence], outputs=[ts_output, ts_info])
            ts_input.change(traffic_sign_detect, inputs=[ts_input, ts_confidence], outputs=[ts_output, ts_info])
        
        # Tab 5: Combined (Autopilot Pro)
        with gr.Tab("🤖 Autopilot Pro (All Models)"):
            with gr.Row():
                gr.Markdown("""
                <div style='text-align: center; padding: 36px; background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border: 3px solid #10b981; border-radius: 20px; margin-bottom: 28px; box-shadow: 0 12px 32px rgba(16, 185, 129, 0.2);'>
                    <h2 style='margin: 0; font-size: 34px; color: #047857; font-weight: 800; letter-spacing: -0.5px;'>🤖 Autopilot Pro - Complete Scene Analysis</h2>
                    <p style='margin: 16px 0 0 0; color: #059669; font-size: 16px; font-weight: 600;'>Run all detection models simultaneously for comprehensive road understanding</p>
                </div>
                """)
            
            with gr.Row():
                with gr.Column(scale=1):
                    with gr.Group():
                        gr.Markdown("### 📤 Upload & Configure")
                        combined_input = gr.Image(type="pil", label="Image Input", height=300)
                        
                        with gr.Accordion("⚙️ Detection Settings", open=True):
                            combined_confidence = gr.Slider(
                                0.1, 1.0, value=0.4, 
                                label="🎯 Global Confidence Threshold",
                                info="Applies to all models simultaneously"
                            )
                            
                            gr.Markdown("""
                            <div style='background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); padding: 18px; border-radius: 12px; margin-top: 12px; border: 1px solid #86efac;'>
                                <strong style='color: #047857; font-size: 16px;'>🎯 All-in-One Detection:</strong><br/>
                                <ul style='margin: 12px 0; padding-left: 20px; font-size: 14px; color: #059669; line-height: 2;'>
                                    <li>🚙 <strong>Vehicles:</strong> LTV & HTV classification</li>
                                    <li>🚶 <strong>Pedestrians:</strong> People detection</li>
                                    <li>🚦 <strong>Traffic Lights:</strong> Signal states</li>
                                    <li>🚸 <strong>Traffic Signs:</strong> 33+ sign types</li>
                                </ul>
                                <div style='margin-top: 12px; padding: 12px; background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); border-radius: 8px; font-size: 13px; color: #047857; font-weight: 600;'>
                                    ⚡ <strong>Performance:</strong> Optimized for real-time multi-model inference
                                </div>
                            </div>
                            """)
                        
                        combined_button = gr.Button(
                            "🚀 Run All Models", 
                            variant="primary", 
                            size="lg"
                        )
                        
                        gr.Markdown("""
                        <div style='text-align: center; margin-top: 16px; padding: 14px; background: linear-gradient(135deg, #10b981 0%, #059669 100%); border-radius: 10px; font-size: 14px; color: white; font-weight: 700; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);'>
                            💡 <strong>Pro Tip:</strong> Best for complete traffic scene analysis
                        </div>
                        """)
                
                with gr.Column(scale=1):
                    with gr.Group():
                        gr.Markdown("### 📊 Comprehensive Detection Results")
                        combined_output = gr.Image(
                            type="pil", 
                            label="All Detections Combined",
                            height=300
                        )
                        
                        with gr.Accordion("📈 Detailed Analysis Report", open=True):
                            combined_info = gr.Textbox(
                                label="Multi-Model Summary", 
                                lines=8,
                                placeholder="Upload an image to see comprehensive detection across all models..."
                            )
                        
                        gr.Markdown("""
                        <div style='margin-top: 12px; padding: 16px; background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%); border-radius: 12px; font-size: 14px; border: 1px solid #e5e7eb;'>
                            <strong style='color: #1a1a1a; font-size: 15px;'>🔍 Color Legend:</strong><br/>
                            <div style='margin-top: 10px; line-height: 2;'>
                                <span style='color: #10b981; font-weight: 700; font-size: 16px;'>●</span> <strong>Green</strong> = Vehicles | 
                                <span style='color: #ef4444; font-weight: 700; font-size: 16px;'>●</span> <strong>Red</strong> = Pedestrians<br/>
                                <span style='color: #f59e0b; font-weight: 700; font-size: 16px;'>●</span> <strong>Orange</strong> = Traffic Lights | 
                                <span style='color: #a855f7; font-weight: 700; font-size: 16px;'>●</span> <strong>Purple</strong> = Traffic Signs
                            </div>
                        </div>
                        """)
            
            combined_button.click(combined_detect, inputs=[combined_input, combined_confidence], outputs=[combined_output, combined_info])
            combined_input.change(combined_detect, inputs=[combined_input, combined_confidence], outputs=[combined_output, combined_info])

# ============================================================================
# LAUNCH
# ============================================================================

if __name__ == "__main__":
    print("🎉 Autopilot Pro is ready!")
    print("🌐 Launching Gradio interface...")
    
    # For local development
    # demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
    
    # For deployment (Hugging Face Spaces, etc.)
    demo.launch(
        favicon_path=str(base_dir / "UI" / "images" / "logo_fyp.png")
    )

