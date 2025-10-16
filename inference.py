"""
Bird Detection Inference Script
Usage: python inference.py --image path/to/image.jpg
"""
from ultralytics import YOLO
import argparse
from pathlib import Path

def detect_birds(image_path, model_path='models/best.pt', conf=0.25):
    """
    Detect birds in an image
    
    Args:
        image_path: Path to input image
        model_path: Path to trained model weights
        conf: Confidence threshold
    """
    # Load model
    model = YOLO(model_path)
    
    # Run detection
    results = model.predict(image_path, save=True, conf=conf)
    
    # Print results
    print(f"\n🐦 Detected Birds in {image_path}:")
    for box in results[0].boxes:
        cls = int(box.cls[0])
        confidence = float(box.conf[0])
        label = model.names[cls]
        print(f"  - {label}: {confidence*100:.1f}% confidence")
    
    print(f"\n✅ Results saved to runs/detect/predict/")
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Detect birds in images')
    parser.add_argument('--image', type=str, required=True, help='Path to image')
    parser.add_argument('--model', type=str, default='models/best.pt', help='Model path')
    parser.add_argument('--conf', type=float, default=0.25, help='Confidence threshold')
    
    args = parser.parse_args()
    detect_birds(args.image, args.model, args.conf)
