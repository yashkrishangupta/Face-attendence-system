// DOM Elements
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const startCameraBtn = document.getElementById('startCamera');
const capturePhotoBtn = document.getElementById('capturePhoto');
const stopCameraBtn = document.getElementById('stopCamera');
const fileInput = document.getElementById('fileInput');
const resultsDiv = document.getElementById('results');
const loadingIndicator = document.getElementById('loadingIndicator');
const trainModelBtn = document.getElementById('trainModel');
const studentsListDiv = document.getElementById('studentsList');

let stream = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadStudents();
});

// Start Camera
startCameraBtn.addEventListener('click', async () => {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
                width: { ideal: 1280 },
                height: { ideal: 720 }
            } 
        });
        video.srcObject = stream;
        
        startCameraBtn.disabled = true;
        capturePhotoBtn.disabled = false;
        stopCameraBtn.disabled = false;
        
        showMessage('Camera started successfully', 'success');
    } catch (error) {
        showMessage('Error accessing camera: ' + error.message, 'error');
    }
});

// Capture Photo
capturePhotoBtn.addEventListener('click', () => {
    if (!stream) {
        showMessage('Please start the camera first', 'error');
        return;
    }
    
    // Set canvas dimensions to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Draw video frame to canvas
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Convert canvas to base64 image
    const imageData = canvas.toDataURL('image/jpeg', 0.95);
    
    // Send to server for recognition
    recognizeFaces(imageData);
});

// Stop Camera
stopCameraBtn.addEventListener('click', () => {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        video.srcObject = null;
        stream = null;
        
        startCameraBtn.disabled = false;
        capturePhotoBtn.disabled = true;
        stopCameraBtn.disabled = true;
        
        showMessage('Camera stopped', 'info');
    }
});

// File Upload
fileInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    
    if (!file) return;
    
    if (!file.type.startsWith('image/')) {
        showMessage('Please select a valid image file', 'error');
        return;
    }
    
    const reader = new FileReader();
    
    reader.onload = (e) => {
        const imageData = e.target.result;
        recognizeFaces(imageData);
    };
    
    reader.readAsDataURL(file);
});

// Recognize Faces
async function recognizeFaces(imageData) {
    loadingIndicator.style.display = 'block';
    resultsDiv.innerHTML = '';
    
    try {
        const response = await fetch('/recognize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageData })
        });
        
        const data = await response.json();
        
        loadingIndicator.style.display = 'none';
        
        if (data.success) {
            displayResults(data);
        } else {
            showMessage('Error: ' + data.message, 'error');
            resultsDiv.innerHTML = `<p class="placeholder">Error: ${data.message}</p>`;
        }
    } catch (error) {
        loadingIndicator.style.display = 'none';
        showMessage('Error processing image: ' + error.message, 'error');
        resultsDiv.innerHTML = `<p class="placeholder">Error processing image</p>`;
    }
}

// Display Results
function displayResults(data) {
    const { recognized_students, unknown_persons, message, attendance, alert } = data;
    
    if (recognized_students.length === 0 && (!unknown_persons || unknown_persons.length === 0)) {
        resultsDiv.innerHTML = `
            <p class="placeholder">
                No faces recognized in the image. Please ensure:
                <br>• The image is clear and well-lit
                <br>• Faces are visible and not obscured
                <br>• The model has been trained with student photos
            </p>
        `;
        showMessage(message, 'info');
        return;
    }
    
    let html = '';
    
    // Show recognized students
    if (recognized_students.length > 0) {
        html += `
            <div style="margin-bottom: 20px;">
                <h3 style="color: #28a745;">✓ ${recognized_students.length} Student(s) Recognized</h3>
                <p style="color: #6c757d; font-size: 0.9em;">Attendance marked successfully</p>
            </div>
        `;
        
        recognized_students.forEach(student => {
            const confidence = (student.confidence * 100).toFixed(1);
            html += `
                <div class="student-card">
                    <h3>${student.student_id}</h3>
                    <p>Confidence: ${confidence}%</p>
                    <p style="color: #28a745; font-weight: 600;">✓ Present</p>
                </div>
            `;
        });
    }
    
    // Show unknown persons alert
    if (unknown_persons && unknown_persons.length > 0) {
        html += `
            <div style="margin-top: 25px; margin-bottom: 20px;">
                <h3 style="color: #dc3545;">⚠️ Security Alert</h3>
                <p style="color: #dc3545; font-size: 0.95em; font-weight: 600;">
                    ${unknown_persons.length} Unknown Person(s) Detected!
                </p>
            </div>
        `;
        
        unknown_persons.forEach((person, index) => {
            html += `
                <div class="unknown-card">
                    <h3>⚠️ Unknown Person #${index + 1}</h3>
                    <p style="color: #dc3545; font-weight: 600;">Not in student database</p>
                    <p style="font-size: 0.85em; color: #6c757d;">Possible security concern</p>
                </div>
            `;
        });
        
        // Show alert message
        showMessage(`⚠️ SECURITY ALERT: ${unknown_persons.length} unknown person(s) detected in classroom!`, 'error');
    }
    
    resultsDiv.innerHTML = html;
    
    if (recognized_students.length > 0 && (!unknown_persons || unknown_persons.length === 0)) {
        showMessage(`${recognized_students.length} student(s) marked present`, 'success');
    }
}

// Train Model
trainModelBtn.addEventListener('click', async () => {
    if (!confirm('This will retrain the model with all student photos. Continue?')) {
        return;
    }
    
    trainModelBtn.disabled = true;
    trainModelBtn.textContent = '⏳ Training...';
    
    try {
        const response = await fetch('/train', {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage(data.message, 'success');
        } else {
            showMessage('Error: ' + data.message, 'error');
        }
    } catch (error) {
        showMessage('Error training model: ' + error.message, 'error');
    } finally {
        trainModelBtn.disabled = false;
        trainModelBtn.textContent = '🔄 Train/Retrain Model';
    }
});

// Load Students List
async function loadStudents() {
    try {
        const response = await fetch('/students');
        const data = await response.json();
        
        if (data.success && data.students.length > 0) {
            let html = '';
            data.students.forEach(student => {
                html += `<div class="student-tag">${student}</div>`;
            });
            studentsListDiv.innerHTML = html;
        } else {
            studentsListDiv.innerHTML = `
                <p class="placeholder">
                    No students registered yet. 
                    <br>Add student photos to the 'student_photos' folder.
                </p>
            `;
        }
    } catch (error) {
        studentsListDiv.innerHTML = `<p class="placeholder">Error loading students</p>`;
    }
}

// Show Message
function showMessage(message, type) {
    const messageBox = document.getElementById('messageBox');
    messageBox.textContent = message;
    messageBox.className = `message-box ${type} show`;
    
    setTimeout(() => {
        messageBox.classList.remove('show');
    }, 4000);
}
