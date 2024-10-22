from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io
import base64
from ultralytics import YOLO
import time
app = Flask(__name__)
CORS(app)
# Dictionary to cache loaded models
loaded_models = {}

# You can customize NMS parameters here
nms_conf = 0.25  # Confidence threshold for NMS
nms_iou = 0.45   # IoU threshold for NMS

# List of model sizes to load
model_sizes = ['yolov8n.pt', 'yolov8s.pt', 'yolov8m.pt', 'yolov8l.pt', 'yolov8x.pt']  # Add your models here

def load_models():
    for model_size in model_sizes:
        try:
            # Load the YOLOv8 model with the specified size
            loaded_models[model_size] = YOLO(f"../model/{model_size.split('.')[0]}_ncnn_model",task="detect")
            print(f"Loaded model: {model_size}")
        except Exception as e:
            print(f"Failed to load model {model_size.split('.')[0]}_ncnn_model: {e}")

@app.route('/predict/<model_size>', methods=['POST'])
def predict(model_size):
    start_time = time.time()
    model_size = f'{model_size}.pt'
    # Check if the requested model is loaded
    if model_size not in loaded_models:
        return jsonify({'error': f'Model {model_size} not loaded'}), 400

    # Get the base64 image from the request body
    data = request.json
    base64_image = data.get('image')

    if not base64_image:
        return jsonify({'error': 'No image provided'}), 400

    # Decode the base64 image
    image_data = base64.b64decode(base64_image)
    image = Image.open(io.BytesIO(image_data))

    # Get the loaded model
    model = loaded_models[model_size]

    # Perform inference on the image
    results = model.predict(image, conf=nms_conf, iou=nms_iou, classes=[0])

    # Process results and draw bounding boxes on the image
    for result in results:
        image = result.plot()  # This will draw bounding boxes on the image
    
    # Convert the processed image back to base64
    image_rgb = image[..., ::-1]
    image = Image.fromarray(image_rgb)
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")  # Save as JPEG
    processed_image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
     # Access the first result
    result = results[0]  # Get the first (and in this case, only) result

    # Retrieve inference times
    inference_time = result.speed   # Inference time
  
    # Retrieve detected classes and format them
    detected_boxes = result.boxes  # Extract boxes
    detections = []
    class_count = {}

    for box in detected_boxes:
        class_id = int(box.cls)  # Class ID of the detected object
        confidence = box.conf  # Confidence score
        class_name = result.names[class_id]  # Get class name from ID

        # Append detection information
        detections.append({
            'class_id': class_id,
            'class_name': class_name,
            'confidence': confidence
        })

        # Count occurrences of each class
        class_count[class_name] = class_count.get(class_name, 0) + 1

    # Prepare a formatted string of detected classes
    detected_classes = ', '.join(f"{count} {name}" for name, count in class_count.items())

    end_time = time.time()
    processing_time = end_time-start_time

    # Return the base64-encoded processed image
    return  jsonify({
        'processing_time': processing_time,
        'predicted_image': processed_image_base64,
        'detections': detected_classes,
        'inference_time': inference_time,
    })


if __name__ == '__main__':
    load_models()  # Load all models at startup
    app.run(host='0.0.0.0', port=5000)
