import gradio as gr
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO
import os

# Paths to models (using dynamic path resolution)
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(script_dir)

MODEL_PATHS = {
    "LTV_HTV": os.path.join(base_dir, "LTV_HTV_Model", "LTV_HTV.pt"),
    "Traffic_Light": os.path.join(base_dir, "Traffic_Light_Model", "epoch70.pt"),
    "Pedestrian": os.path.join(base_dir, "Pedestrian_Model", "last.pt"),
    "Traffic_Sign": os.path.join(base_dir, "TRAFFIC_SIGN_MODEL", "trafic.pt")
}
# Load all models
def load_models():
    models = {}
    for name, path in MODEL_PATHS.items():
        if not os.path.exists(path):
            raise FileNotFoundError(f"❌ Model file not found at {path}")
        try:
            models[name] = YOLO(path)
            print(f"✅ {name} model loaded successfully!")
        except Exception as e:
            raise RuntimeError(f"❌ Error loading {name} model: {e}")
    return models

models = load_models()

# Function to run combined predictions
def predict(image):
    try:
        print("🔄 Running YOLO detections on all models...")
        img_array = np.array(image.convert('RGB'))  # Convert PIL image to numpy array
        
        detected_objects = 0

        for model_name, model in models.items():
            results = model(img_array)  # Perform inference

            for result in results:
                print(f"📸 {model_name} detected {len(result.boxes)} objects")
                
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    confidence = float(box.conf[0]) if box.conf is not None else 0
                    cls_index = int(box.cls[0]) if box.cls is not None else -1

                    if confidence < 0.4 or cls_index == -1:
                        print(f"⚠️ Low confidence ({confidence:.2f}) - Skipping detection")
                        continue

                    label = model.names[cls_index] if hasattr(model, "names") and cls_index in model.names else f"Class_{cls_index}"
                    
                    print(f"✅ {model_name} detected: {label} ({confidence:.2f}) at [{x1}, {y1}, {x2}, {y2}]")
                    detected_objects += 1
                    
                    # Draw bounding box & label on image
                    color = (0, 255, 0) if model_name == "LTV_HTV" else (255, 0, 0) if model_name == "Traffic_Light" else (0, 0, 255)
                    cv2.rectangle(img_array, (x1, y1), (x2, y2), color, 3)
                    label_text = f"{label} {confidence:.2f}"
                    cv2.putText(img_array, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA)

        if detected_objects == 0:
            print("🚫 No objects detected!")

        result_image = Image.fromarray(img_array)
        return result_image
    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        return None

# Flag to control camera feed
stop_camera = False

def process_camera_feed():
    global stop_camera
    stop_camera = False
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        raise RuntimeError("⚠️ Camera not working!")
    
    while not stop_camera:
        ret, frame = cap.read()
        if not ret:
            break

        for model_name, model in models.items():
            results = model(frame)

            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    confidence = float(box.conf[0]) if box.conf is not None else 0
                    cls_index = int(box.cls[0]) if box.cls is not None else -1

                    if confidence < 0.7 or cls_index == -1:
                        continue

                    label = model.names[cls_index] if hasattr(model, "names") and cls_index in model.names else f"Class_{cls_index}"
                    
                    color = (0, 255, 0) if model_name == "LTV_HTV" else (255, 0, 0) if model_name == "Traffic_Light" else (0, 0, 255)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
                    label_text = f"{label} {confidence:.2f}"
                    cv2.putText(frame, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        yield Image.fromarray(frame_rgb)
    
    cap.release()

def stop_camera_feed():
    global stop_camera
    stop_camera = True

# Gradio interface
with gr.Blocks() as demo:
    
    with gr.Tab("📷 Upload Image"):
        upload_box = gr.Image(label="Upload Image", type="pil")
        output_image = gr.Image(label="Detection Result", type="pil")
        upload_box.change(predict, inputs=upload_box, outputs=output_image)
    
    with gr.Tab("📹 Live Camera"):
        camera_output = gr.Image(label="Live Detection")
        start_button = gr.Button("Start Camera")
        stop_button = gr.Button("Stop Camera")
        
        start_button.click(process_camera_feed, outputs=camera_output, show_progress=False)
        stop_button.click(stop_camera_feed)

# Launch the app
demo.launch(server_port=7868, share=True)
