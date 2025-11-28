"""
Flask API for Bird Detection
"""
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image
import gdown
import os
import io
import base64
import numpy as np
import cv2

app = Flask(__name__)
CORS(app)

# Global model variable
model = None

def load_model():
    """Load the YOLO model (cached)"""
    global model
    if model is None:
        model_path = 'best.pt'
        
        # Download if not exists
        if not os.path.exists(model_path):
            file_id = "1SjfGJ3UUgWQ_V95TLWoWsmkNk-VaAXkv"
            url = f'https://drive.google.com/uc?id={file_id}'
            gdown.download(url, model_path, quiet=False)
        
        model = YOLO(model_path)
    
    return model

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

@app.route('/detect', methods=['POST'])
def detect():
    """Detect birds in uploaded image"""
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No image file selected"}), 400
        
        # Load model
        model = load_model()
        
        # Read image
        image = Image.open(file.stream)
        
        # Convert PIL to numpy array
        image_np = np.array(image)
        
        # Run detection
        results = model.predict(image_np, conf=0.25, verbose=False)
        
        # Get result image with bounding boxes
        result_img = results[0].plot()
        
        # Convert BGR to RGB for display
        result_img_rgb = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
        
        # Encode result image to base64
        result_pil = Image.fromarray(result_img_rgb)
        buffer = io.BytesIO()
        result_pil.save(buffer, format='PNG')
        result_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        # Extract detections
        detections = []
        for box in results[0].boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            label = model.names[cls]
            detections.append({
                "species": label,
                "confidence": round(conf * 100, 1)
            })
        
        return jsonify({
            "success": True,
            "detections": detections,
            "result_image": f"data:image/png;base64,{result_base64}",
            "count": len(detections)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

