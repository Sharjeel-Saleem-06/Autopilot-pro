import gradio as gr
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO
import os

# Load YOLO model
def load_model():
    # Use dynamic path resolution (works on any system)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, "epoch70.pt")
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"❌ Model file not found at {model_path}")
    
    try:
        model = YOLO(model_path)
        print("✅ Model loaded successfully!")
        return model
    except Exception as e:
        raise RuntimeError(f"❌ Error loading model: {e}")

model = load_model()

# Function to perform inference on an image
def predict(image):
    try:
        print("🔄 Running YOLO detection...")
        img_array = np.array(image.convert('RGB'))  # Convert PIL image to numpy array
        results = model(img_array)  # Perform inference
        
        detected_objects = 0  # Counter for detected objects
        
        for result in results:
            print(f"📸 Detected {len(result.boxes)} objects")
            
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
                confidence = float(box.conf[0]) if box.conf is not None else 0
                cls_index = int(box.cls[0]) if box.cls is not None else -1
                
                # Check if confidence is high enough
                if confidence < 0.5 or cls_index == -1:
                    print(f"⚠️ Low confidence ({confidence:.2f}) - Skipping detection")
                    continue
                
                # Retrieve label (Check if model has names)
                if hasattr(model, "names") and cls_index in model.names:
                    label = model.names[cls_index]
                else:
                    label = f"Class_{cls_index}"  # Fallback in case class names are missing
                
                print(f"✅ Object detected: {label} ({confidence:.2f}) at [{x1}, {y1}, {x2}, {y2}]")
                detected_objects += 1
                
                # Draw bounding box & label on image
                cv2.rectangle(img_array, (x1, y1), (x2, y2), (0, 255, 0), 3)
                label_text = f"{label} {confidence:.2f}"
                cv2.putText(img_array, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)
        
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

        results = model(frame)
        
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0]) if box.conf is not None else 0
                cls_index = int(box.cls[0]) if box.cls is not None else -1

                if confidence < 0.7 or cls_index == -1:
                    continue

                if hasattr(model, "names") and cls_index in model.names:
                    label = model.names[cls_index]
                else:
                    label = f"Class_{cls_index}"

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                label_text = f"{label} {confidence:.2f}"
                cv2.putText(frame, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)

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
demo.launch( server_port=7862, share=True)
