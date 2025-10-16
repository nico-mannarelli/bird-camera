# 🐦 Bird Detection with YOLOv8

A deep learning model for real-time bird species detection and classification, trained on the NABirds dataset using AWS SageMaker.

## 🎯 Project Overview

This project implements a computer vision system that can:
- Detect multiple birds in images with bounding boxes
- Classify bird species with confidence scores
- Process images in real-time (~309ms per image)
- Handle complex scenes with multiple bird species

**Trained on:** NABirds dataset (555 North American bird species)  
**Architecture:** YOLOv8 (You Only Look Once v8)  
**Training:** 50 epochs on AWS SageMaker (ml.g4dn.xlarge GPU)  
**Performance:** [Add your mAP score here]

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/yourusername/bird-cam-project.git
cd bird-cam-project
pip install -r requirements.txt
```

### Run Detection
```bash
# Detect birds in an image
python inference.py --image path/to/your/image.jpg

# Adjust confidence threshold
python inference.py --image bird.jpg --conf 0.5
```

### Python API
```python
from ultralytics import YOLO

# Load model
model = YOLO('models/best.pt')

# Run detection
results = model.predict('image.jpg', save=True)

# Access detections
for box in results[0].boxes:
    print(f"Species: {model.names[int(box.cls[0])]}")
    print(f"Confidence: {float(box.conf[0]):.2f}")
```

## 📊 Results

### Training Performance

![Training Curves](results/training_curves.png)

**Key Metrics:**
- Final Loss: [Add from results.csv]
- mAP@50: [Add from results.csv]
- mAP@50-95: [Add from results.csv]
- Training Time: 11 hours on AWS GPU

### Example Detections

![Example Detections](results/example_detections.jpg)

Successfully detects and classifies multiple bird species including:
- Black Scoter (Male)
- Northern Gannet
- House Sparrow
- Royal Tern
- And 551+ other species

### Confusion Matrix

![Confusion Matrix](results/confusion_matrix.png)

## 🛠️ Technical Details

### Architecture
- **Base Model:** YOLOv8n (Nano - optimized for speed)
- **Input Size:** 640x640
- **Batch Size:** 16
- **Optimizer:** AdamW
- **Epochs:** 50

### Training Infrastructure
- **Platform:** AWS SageMaker
- **Instance:** ml.g4dn.xlarge (NVIDIA T4 GPU)
- **Storage:** S3 for dataset and model artifacts
- **Total Cost:** ~$8 for full training run

### Dataset
- **Source:** NABirds Dataset
- **Species:** 555 North American bird species
- **Images:** [Add number] training images
- **Format:** YOLO format (converted from original)

## 📁 Project Structure
```
bird-cam-project/
├── inference.py          # Detection script
├── train.py             # Training script
├── models/
│   └── best.pt          # Trained weights (23MB)
├── results/             # Training visualizations
└── notebooks/           # Jupyter notebooks
```

## 🎓 What I Learned

- **AWS SageMaker:** Setting up training jobs, managing compute resources, S3 integration
- **Computer Vision:** Object detection, YOLO architecture, transfer learning
- **ML Ops:** Model versioning, experiment tracking, cloud deployment
- **Data Engineering:** Dataset preprocessing, format conversion, data pipelines

## 🔮 Future Improvements

- [ ] Deploy as REST API using AWS Lambda
- [ ] Build web interface with Streamlit
- [ ] Add real-time video detection
- [ ] Fine-tune on specific bird species
- [ ] Implement model quantization for edge devices
- [ ] Add data augmentation for better generalization

## 📝 License

MIT License - feel free to use for your own projects!

## 🤝 Acknowledgments

- NABirds Dataset creators
- Ultralytics YOLOv8 team
- AWS SageMaker documentation

## 📧 Contact

[Your Name] - [Your Email/LinkedIn]

Project Link: [https://github.com/yourusername/bird-cam-project](https://github.com/yourusername/bird-cam-project)
