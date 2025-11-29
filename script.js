// API endpoint - Uses Netlify Functions
// For local development with Netlify Dev: use relative paths
// For production: Netlify Functions are automatically available at /.netlify/functions/
const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const API_BASE = isLocalhost 
    ? 'http://localhost:8888/.netlify/functions'  // Local Netlify Dev
    : '/.netlify/functions';  // Production - Netlify Functions

const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const resultsSection = document.getElementById('resultsSection');
const loading = document.getElementById('loading');
const error = document.getElementById('error');
const originalImage = document.getElementById('originalImage');
const resultImage = document.getElementById('resultImage');
const detectionsList = document.getElementById('detectionsList');

// Click to upload
uploadArea.addEventListener('click', () => {
    fileInput.click();
});

// File input change
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

// Drag and drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    if (e.dataTransfer.files.length > 0) {
        handleFile(e.dataTransfer.files[0]);
    }
});

async function handleFile(file) {
    // Validate file type
    if (!file.type.match('image/jpeg') && !file.type.match('image/png')) {
        showError('Please upload a JPG, JPEG, or PNG image.');
        return;
    }

    // Show loading
    loading.style.display = 'block';
    resultsSection.style.display = 'none';
    error.style.display = 'none';

    // Display original image
    const reader = new FileReader();
    reader.onload = async (e) => {
        originalImage.src = e.target.result;
        
        // Convert image to base64 for Netlify Functions
        const base64Image = e.target.result; // Already includes data:image/... prefix
        
        try {
            const response = await fetch(`${API_BASE}/detect`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    image: base64Image
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Detection failed');
            }

            const data = await response.json();

            if (data.success) {
                // Display result image
                resultImage.src = data.result_image;

                // Display detections
                displayDetections(data.detections);

                // Show results
                resultsSection.style.display = 'block';
            } else {
                throw new Error('Detection failed');
            }
        } catch (err) {
            showError(`Error: ${err.message}`);
        } finally {
            loading.style.display = 'none';
        }
    };
    reader.readAsDataURL(file);
}

function displayDetections(detections) {
    if (detections.length === 0) {
        detectionsList.innerHTML = '<p style="color: #999; padding: 20px; text-align: center;">No birds detected. Try a different image!</p>';
        return;
    }

    detectionsList.innerHTML = detections.map((detection, index) => `
        <div class="detection-item">
            <span class="detection-species">Detection ${index + 1}: ${detection.species}</span>
            <span class="detection-confidence">${detection.confidence}% confidence</span>
        </div>
    `).join('');
}

function showError(message) {
    error.textContent = message;
    error.style.display = 'block';
    loading.style.display = 'none';
}

