import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np

st.set_page_config(page_title="Bird Species Detector", page_icon="🐦")

st.title("🐦 Bird Species Detector")
st.write("Upload an image to detect and classify bird species using YOLOv8")

# Load model (cached so it only loads once)
@st.cache_resource
def load_model():
    return YOLO('bird_detection/weights/best.pt')

model = load_model()

# File uploader
uploaded_file = st.file_uploader("Choose a bird image...", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    # Display original image
    image = Image.open(uploaded_file)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Image")
        st.image(image, use_container_width=True)
    
    # Run detection
    with st.spinner('🔍 Detecting birds...'):
        results = model.predict(image, conf=0.25)
        result_img = results[0].plot()
    
    with col2:
        st.subheader("Detection Results")
        st.image(result_img[..., ::-1], use_container_width=True)
    
    # Display detections
    st.subheader("Detected Species:")
    if len(results[0].boxes) > 0:
        for i, box in enumerate(results[0].boxes):
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            label = model.names[cls]
            
            st.metric(
                label=f"Detection {i+1}",
                value=label,
                delta=f"{conf*100:.1f}% confidence"
            )
    else:
        st.warning("No birds detected. Try a different image!")

# Sidebar info
with st.sidebar:
    st.header("About")
    st.write("""
    This bird detector uses YOLOv8 trained on the NABirds dataset 
    with 555 North American bird species.
    
    **Model Stats:**
    - Architecture: YOLOv8n
    - Training: 50 epochs on AWS SageMaker
    - Inference: ~300ms per image
    """)
    
    st.header("How to Use")
    st.write("""
    1. Upload a bird image (JPG, JPEG, or PNG)
    2. Wait for detection (~1 second)
    3. View results with bounding boxes and species labels
    """)

