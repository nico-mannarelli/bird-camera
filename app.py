import streamlit as st
import os
import sys

# Set OpenCV environment variables before importing (fixes headless issues)
os.environ['OPENCV_IO_ENABLE_OPENEXR'] = '0'
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
os.environ['OPENCV_IO_ENABLE_JASPER'] = '0'
os.environ['OPENCV_LOG_LEVEL'] = 'ERROR'

# Workaround for libGL issue on Streamlit Cloud
# Try to import cv2 with error suppression
try:
    import cv2
    # Force OpenCV to use headless mode
    cv2.setNumThreads(0)
except Exception as e:
    # If cv2 import fails, try to continue anyway
    # Ultralytics might still work
    pass

try:
    from ultralytics import YOLO
except ImportError as e:
    # Show a more helpful error message
    error_msg = str(e)
    if 'libGL' in error_msg:
        st.error("""
        **OpenCV Library Error**
        
        The app is having trouble loading OpenCV due to missing system libraries.
        This is a known issue with Streamlit Cloud.
        
        **Possible solutions:**
        1. Try refreshing the page
        2. Wait a few minutes and try again (Streamlit Cloud may need to install dependencies)
        3. Contact Streamlit support if the issue persists
        
        **Error details:** libGL.so.1 library not found
        """)
    else:
        st.error(f"Failed to import YOLO: {e}")
    st.stop()

from PIL import Image
import gdown
import io
import time
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Bird Species Detector", 
    page_icon="🐦",
    layout="wide"
)

# Initialize session state for detection history
if 'detection_history' not in st.session_state:
    st.session_state.detection_history = []

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
    .bird-info-card {
        padding: 1rem;
        border-left: 4px solid #1f77b4;
        background-color: #f0f2f6;
        border-radius: 0.25rem;
        margin: 0.5rem 0;
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

def get_bird_info_url(bird_name):
    """Generate Wikipedia URL for bird species"""
    # Clean bird name for URL
    url_name = bird_name.replace(" ", "_").replace("(", "").replace(")", "")
    return f"https://en.wikipedia.org/wiki/{url_name}"

def get_allaboutbirds_url(bird_name):
    """Generate AllAboutBirds URL (approximate)"""
    # AllAboutBirds uses different URL structure, this is a search link
    search_name = bird_name.replace(" ", "+")
    return f"https://www.allaboutbirds.org/guide/{search_name}"

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
    
    # Detection History
    st.header("📚 Detection History")
    if st.session_state.detection_history:
        st.write(f"**{len(st.session_state.detection_history)} detection(s) saved**")
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.detection_history = []
            st.rerun()
        
        # Show recent detections
        st.write("**Recent detections:**")
        for i, hist in enumerate(reversed(st.session_state.detection_history[-5:]), 1):
            with st.expander(f"Detection #{len(st.session_state.detection_history) - len(st.session_state.detection_history[-5:]) + i}: {hist['timestamp']}"):
                st.write(f"**Species:** {', '.join(hist['species'])}")
                st.write(f"**Count:** {hist['count']} bird(s)")
                st.write(f"**Confidence:** {hist['avg_confidence']:.1f}%")
    else:
        st.info("No detections saved yet. Upload an image to start!")
    
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
    # Display image metadata
    image = Image.open(uploaded_file)
    image_size = len(uploaded_file.getvalue())
    image_format = image.format or "Unknown"
    
    # Show metadata in expander
    with st.expander("📊 Image Information"):
        col_meta1, col_meta2, col_meta3 = st.columns(3)
        with col_meta1:
            st.metric("Dimensions", f"{image.width} × {image.height}")
        with col_meta2:
            st.metric("File Size", f"{image_size / 1024:.1f} KB")
        with col_meta3:
            st.metric("Format", image_format)
    
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
        # Store detection data for history
        detections_data = []
        species_list = []
        confidences = []
        
        # Create columns for detection cards
        num_detections = len(results[0].boxes)
        cols = st.columns(min(3, num_detections))
        
        for i, box in enumerate(results[0].boxes):
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            label = model.names[cls]
            species_list.append(label)
            confidences.append(conf)
            
            # Get bounding box coordinates
            box_coords = box.xyxy[0].cpu().numpy()
            
            detections_data.append({
                'species': label,
                'confidence': conf,
                'bbox': box_coords.tolist()
            })
            
            with cols[i % len(cols)]:
                st.metric(
                    label=f"Detection {i+1}",
                    value=label,
                    delta=f"{conf*100:.1f}% confidence"
                )
        
        # Bird Information Cards
        st.markdown("---")
        st.subheader("📖 Bird Information")
        
        unique_species = list(set(species_list))
        for species in unique_species:
            with st.expander(f"🐦 {species} - Learn More"):
                col_info1, col_info2 = st.columns(2)
                
                with col_info1:
                    st.write(f"**Species:** {species}")
                    # Get detections for this species
                    species_detections = [d for d in detections_data if d['species'] == species]
                    st.write(f"**Detected:** {len(species_detections)} time(s)")
                    if species_detections:
                        avg_conf = sum(d['confidence'] for d in species_detections) / len(species_detections)
                        st.write(f"**Average Confidence:** {avg_conf*100:.1f}%")
                
                with col_info2:
                    st.write("**Learn More:**")
                    wiki_url = get_bird_info_url(species)
                    st.markdown(f"[🌐 Wikipedia]({wiki_url})")
                    
                    # Try to create a search link for AllAboutBirds
                    search_url = f"https://www.allaboutbirds.org/search/?q={species.replace(' ', '+')}"
                    st.markdown(f"[🐦 All About Birds (Search)]({search_url})")
                
                st.write("---")
                st.write("**About this species:**")
                st.info("""
                This bird is part of the NABirds dataset with 555 North American bird species. 
                For detailed information about habitat, diet, behavior, and conservation status, 
                visit the links above.
                """)
        
        # Export annotated image
        st.markdown("---")
        st.subheader("💾 Export Results")
        
        # Convert result image to bytes for download
        result_pil = Image.fromarray(result_img[..., ::-1])
        img_buffer = io.BytesIO()
        result_pil.save(img_buffer, format='PNG')
        img_bytes = img_buffer.getvalue()
        
        col_download1, col_download2, col_download3 = st.columns(3)
        
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
                label="📄 Download Detection Data (TXT)",
                data=detection_text.encode('utf-8'),
                file_name=f"bird_detections_{int(time.time())}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col_download3:
            # Export as JSON
            import json
            json_data = {
                'timestamp': datetime.now().isoformat(),
                'image_info': {
                    'width': image.width,
                    'height': image.height,
                    'format': image_format,
                    'size_kb': round(image_size / 1024, 2)
                },
                'detections': detections_data,
                'inference_time_ms': round(inference_time * 1000, 2),
                'confidence_threshold': confidence
            }
            json_str = json.dumps(json_data, indent=2)
            
            st.download_button(
                label="📋 Download Detection Data (JSON)",
                data=json_str.encode('utf-8'),
                file_name=f"bird_detections_{int(time.time())}.json",
                mime="application/json",
                use_container_width=True
            )
        
        # Save to history button
        st.markdown("---")
        if st.button("💾 Save to Detection History", use_container_width=True):
            history_entry = {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'species': species_list,
                'count': num_detections,
                'avg_confidence': sum(confidences) / len(confidences) * 100,
                'confidence_threshold': confidence,
                'inference_time': round(inference_time * 1000, 2)
            }
            st.session_state.detection_history.append(history_entry)
            st.success(f"✅ Saved to history! ({len(st.session_state.detection_history)} total)")
            st.rerun()
        
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
