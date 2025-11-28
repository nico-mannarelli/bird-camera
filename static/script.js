// API endpoint - change this to your deployed backend URL
const API_URL = window.location.origin.includes('netlify') 
    ? 'https://your-backend-url.railway.app' // Replace with your backend URL
    : 'http://localhost:5000';

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
    reader.onload = (e) => {
        originalImage.src = e.target.result;
    };
    reader.readAsDataURL(file);

    // Create form data
    const formData = new FormData();
    formData.append('image', file);

    try {
        const response = await fetch(`${API_URL}/detect`, {
            method: 'POST',
            body: formData
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

