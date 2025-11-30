import streamlit as st
from ultralytics import YOLO
from PIL import Image
import gdown
import os
import io
import time

# Page config with dark mode support
st.set_page_config(
    page_title="Bird Species Detector", 
    page_icon="🐦",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
    }
    .detection-card {
        background-color: var(--background-color);
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

st.title("🐦 Bird Species Detector")
st.write("Upload an image to detect and classify bird species using YOLOv8")

# Load model (cached so it only loads once)
@st.cache_resource
def load_model():
    model_path = 'best.pt'
    
    # Download if not exists
    if not os.path.exists(model_path):
        with st.spinner("⬇️ Downloading model (first time only, ~23MB)..."):
            file_id = "1SjfGJ3UUgWQ_V95TLWoWsmkNk-VaAXkv"
            url = f'https://drive.google.com/uc?id={file_id}'
            
            try:
                gdown.download(url, model_path, quiet=False)
                st.success("✅ Model downloaded!")
            except Exception as e:
                st.error(f"Failed to download model: {e}")
                st.stop()
    
    return YOLO(model_path)

model = load_model()

# Sidebar with settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Confidence threshold slider
    confidence = st.slider(
        "Confidence Threshold",
        min_value=0.1,
        max_value=1.0,
        value=0.25,
        step=0.05,
        help="Adjust the minimum confidence level for detections. Lower values show more detections but may include false positives."
    )
    
    st.markdown("---")
    st.header("ℹ️ About")
    st.write("""
    This bird detector uses YOLOv8 trained on the NABirds dataset 
    with 555 North American bird species.
    
    **Model Stats:**
    - Architecture: YOLOv8n
    - Training: 50 epochs on AWS SageMaker
    - Inference: ~300ms per image
    """)
    
    st.header("📖 How to Use")
    st.write("""
    1. Upload a bird image (JPG, JPEG, or PNG)
    2. Adjust confidence threshold if needed
    3. Wait for detection (~1 second)
    4. View results with bounding boxes and species labels
    5. Download the annotated image
    """)

# File uploader
uploaded_file = st.file_uploader("Choose a bird image...", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    # Display original image
    image = Image.open(uploaded_file)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📷 Original Image")
        st.image(image, use_container_width=True)
    
    # Run detection with user-selected confidence
    with st.spinner('🔍 Detecting birds...'):
        start_time = time.time()
        results = model.predict(image, conf=confidence, verbose=False)
        inference_time = time.time() - start_time
        result_img = results[0].plot()
    
    with col2:
        st.subheader("🎯 Detection Results")
        st.image(result_img[..., ::-1], use_container_width=True)
        
        # Show inference time
        st.caption(f"⏱️ Inference time: {inference_time*1000:.0f}ms")
    
    # Display detections
    st.markdown("---")
    st.subheader("🐦 Detected Species:")
    
    if len(results[0].boxes) > 0:
        # Create columns for detection cards
        num_detections = len(results[0].boxes)
        cols = st.columns(min(3, num_detections))
        
        for i, box in enumerate(results[0].boxes):
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            label = model.names[cls]
            
            with cols[i % len(cols)]:
                st.metric(
                    label=f"Detection {i+1}",
                    value=label,
                    delta=f"{conf*100:.1f}% confidence"
                )
        
        # Export annotated image
        st.markdown("---")
        st.subheader("💾 Export Results")
        
        # Convert result image to bytes for download
        result_pil = Image.fromarray(result_img[..., ::-1])
        img_buffer = io.BytesIO()
        result_pil.save(img_buffer, format='PNG')
        img_bytes = img_buffer.getvalue()  # Get actual bytes for download
        
        col_download1, col_download2 = st.columns(2)
        
        with col_download1:
            st.download_button(
                label="📥 Download Annotated Image",
                data=img_bytes,
                file_name=f"bird_detection_{int(time.time())}.png",
                mime="image/png",
                use_container_width=True
            )
        
        with col_download2:
            # Export detection data as text
            detection_text = "\n".join([
                f"Detection {i+1}: {model.names[int(box.cls[0])]} ({float(box.conf[0])*100:.1f}% confidence)"
                for i, box in enumerate(results[0].boxes)
            ])
            
            st.download_button(
                label="📄 Download Detection Data",
                data=detection_text.encode('utf-8'),  # Encode text to bytes
                file_name=f"bird_detections_{int(time.time())}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        # Summary stats
        st.info(f"✅ Found {num_detections} bird(s) with confidence ≥ {confidence*100:.0f}%")
        
    else:
        st.warning(f"⚠️ No birds detected with confidence ≥ {confidence*100:.0f}%. Try:")
        st.write("- Lowering the confidence threshold")
        st.write("- Using a clearer bird image")
        st.write("- Ensuring the bird is clearly visible in the image")

else:
    # Show example or instructions when no image is uploaded
    st.info("👆 Upload an image above to get started!")
    
    # Optional: Show example images or tips
    with st.expander("💡 Tips for best results"):
        st.write("""
        - **Clear images work best**: Make sure the bird is clearly visible
        - **Good lighting**: Well-lit photos improve detection accuracy
        - **Single bird focus**: Images with one main bird work better than crowded scenes
        - **Adjust confidence**: Lower the threshold if no birds are detected
        - **Multiple angles**: Try different photos if detection fails
        """)
