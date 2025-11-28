# Face Recognition Attendance System

A web-based attendance system that uses face recognition to automatically mark student attendance. Built with Flask, Python, and scikit-learn.

## Features

- 📸 **Real-time Face Recognition**: Capture class photos via webcam or upload images
- 👥 **Multi-Face Detection**: Recognize multiple students in a single photo
- 📊 **Attendance Tracking**: Automatic attendance marking with timestamps
- 🎓 **Student Management**: Support for multiple students (initially configured for 10)
- 📅 **Attendance History**: View daily and historical attendance records
- 🔄 **Model Training**: Easy retraining when adding new students

## Prerequisites

- Python 3.8 or higher
- Webcam (for live capture)
- Windows/Linux/macOS

## Installation

1. **Navigate to the project directory**:
   ```bash
   cd face-attendance-system
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   **Note**: Installing `dlib` might require additional setup:
   - **Windows**: Install Visual Studio Build Tools or use pre-built wheels
   - **Linux**: `sudo apt-get install cmake libboost-all-dev`
   - **macOS**: `brew install cmake boost`

## Setting Up Student Photos

1. Create a folder for each student in the `student_photos` directory:
   ```
   student_photos/
   ├── Student_001/
   │   ├── photo1.jpg
   │   ├── photo2.jpg
   │   └── photo3.jpg
   ├── Student_002/
   │   ├── photo1.jpg
   │   └── photo2.jpg
   └── ...
   ```

2. **Folder naming convention**: Use student IDs or names (e.g., `Student_001`, `John_Doe`, etc.)

3. **Photo guidelines**:
   - Use 3-5 photos per student for better accuracy
   - Clear, front-facing photos
   - Good lighting
   - Different expressions/angles
   - Supported formats: JPG, JPEG, PNG

4. **Example structure for 10 students**:
   ```
   student_photos/
   ├── Student_001/
   ├── Student_002/
   ├── Student_003/
   ├── Student_004/
   ├── Student_005/
   ├── Student_006/
   ├── Student_007/
   ├── Student_008/
   ├── Student_009/
   └── Student_010/
   ```

## Running the Application

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Access the application**:
   Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

3. **Train the model** (first time or when adding new students):
   - Click on "Train/Retrain Model" button in the main interface
   - Wait for training to complete

## Usage

### Taking Attendance

1. **Using Webcam**:
   - Click "Start Camera"
   - Position students in frame
   - Click "Capture & Mark Attendance"
   - View recognized students in the results panel

2. **Using Photo Upload**:
   - Click "Upload Class Photo"
   - Select a class photo from your computer
   - System will automatically recognize and mark attendance

### Viewing Attendance

1. Navigate to "View Attendance" tab
2. Click "Today's Attendance" for current day
3. Click "All Records" to see historical data

## Project Structure

```
face-attendance-system/
├── app.py                      # Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── static/
│   ├── css/
│   │   └── style.css          # Styling
│   └── js/
│       ├── app.js             # Main page JavaScript
│       └── attendance.js      # Attendance page JavaScript
├── templates/
│   ├── index.html             # Main page
│   └── attendance.html        # Attendance records page
├── student_photos/            # Student photos (organized by student ID)
├── attendance_records/        # JSON files with attendance data
├── face_recognition_model.pkl # Trained model (generated)
└── face_encodings.pkl         # Face encodings (generated)
```

## How It Works

1. **Face Encoding**: Each student photo is converted to a 128-dimensional face encoding
2. **Model Training**: KNN classifier is trained with student face encodings
3. **Recognition**: When a class photo is captured:
   - System detects all faces in the image
   - Compares each face with trained encodings
   - Identifies students based on similarity
4. **Attendance**: Recognized students are automatically marked present with timestamp

## Customization

### Adding More Students

1. Create new folders in `student_photos/` with student IDs
2. Add 3-5 photos for each new student
3. Click "Train/Retrain Model" in the web interface

### Adjusting Recognition Threshold

In `app.py`, modify the threshold value (line ~120):
```python
threshold = 0.6  # Lower = stricter matching, Higher = more lenient
```

## Troubleshooting

### Camera not working
- Check browser permissions for camera access
- Ensure no other application is using the camera

### Poor recognition accuracy
- Add more photos per student (3-5 recommended)
- Ensure photos are clear and well-lit
- Retrain the model after adding photos
- Adjust recognition threshold

### Installation issues with dlib
- Windows: Download pre-built wheel from https://github.com/z-mahmud22/Dlib_Windows_Python3.x
- Or use: `pip install dlib-binary`

## Technologies Used

- **Backend**: Flask, Python
- **Face Recognition**: face_recognition library (based on dlib)
- **Machine Learning**: scikit-learn (KNN classifier)
- **Computer Vision**: OpenCV
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Storage**: JSON files

## Security Notes

- This is a basic implementation for educational purposes
- For production use, consider:
  - Adding user authentication
  - Encrypting sensitive data
  - Using a proper database
  - Implementing access controls

## License

This project is open-source and available for educational purposes.

## Support

For issues or questions, please check:
1. Photo quality and organization
2. Model training completion
3. Browser console for JavaScript errors
4. Terminal for Python errors

---

**Note**: Make sure to populate the `student_photos` folder with actual student photos before using the system!
