import os
from ultralytics import YOLO

data_dir = '/opt/ml/input/data/training'
model = YOLO('yolov8n.pt')

model.train(
    data=os.path.join(data_dir, 'dataset.yaml'),
    epochs=50,
    imgsz=640,
    batch=16,
    project='/opt/ml/model',
    name='bird_detection',
    device=0
)
