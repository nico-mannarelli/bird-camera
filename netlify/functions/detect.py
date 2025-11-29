"""
Netlify Function for Bird Detection
Note: Netlify Functions have a 10s timeout (free) or 26s (pro)
First request will be slow due to model loading
"""
import json
import os
import sys
import base64
import io

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from ultralytics import YOLO
    from PIL import Image
    import gdown
    import numpy as np
    import cv2
except ImportError as e:
    print(f"Import error: {e}")

# Global model cache (persists across invocations in same container)
model = None
model_path = '/tmp/best.pt'

def load_model():
    """Load the YOLO model (cached across invocations)"""
    global model
    if model is None:
        # Download model if not exists
        if not os.path.exists(model_path):
            print("Downloading model...")
            file_id = "1SjfGJ3UUgWQ_V95TLWoWsmkNk-VaAXkv"
            url = f'https://drive.google.com/uc?id={file_id}'
            gdown.download(url, model_path, quiet=False)
            print("Model downloaded")
        
        print("Loading model...")
        model = YOLO(model_path)
        print("Model loaded")
    
    return model

def handler(event, context):
    """Netlify Function handler"""
    try:
        # Handle CORS preflight
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS'
                },
                'body': ''
            }
        
        # Only handle POST requests
        if event.get('httpMethod') != 'POST':
            return {
                'statusCode': 405,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({"error": "Method not allowed"})
            }
        
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        
        # Check if image data is provided
        if 'image' not in body:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({"error": "No image data provided"})
            }
        
        # Decode base64 image
        image_data = body['image']
        if image_data.startswith('data:image'):
            # Remove data URL prefix
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Load model (cached)
        model = load_model()
        
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
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                "success": True,
                "detections": detections,
                "result_image": f"data:image/png;base64,{result_base64}",
                "count": len(detections)
            })
        }
    
    except Exception as e:
        import traceback
        error_msg = str(e)
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({"error": error_msg})
        }

