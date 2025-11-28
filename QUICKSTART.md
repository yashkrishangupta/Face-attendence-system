# Quick Start Guide

## Step 1: Install Dependencies

Open a terminal in the project directory and run:

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

**Note**: If you encounter issues installing `dlib`, you can try:
```bash
pip install dlib-binary
```

## Step 2: Add Student Photos

1. Navigate to the `student_photos` folder
2. Create a folder for each student (e.g., Student_001, Student_002, etc.)
3. Add 3-5 clear photos of each student in their respective folders
4. Supported formats: .jpg, .jpeg, .png

Example:
```
student_photos/
├── Student_001/
│   ├── photo1.jpg
│   ├── photo2.jpg
│   └── photo3.jpg
├── Student_002/
│   └── ...
```

## Step 3: Run the Application

```bash
python app.py
```

The server will start at: http://localhost:5000

## Step 4: Train the Model

1. Open http://localhost:5000 in your browser
2. Click the "Train/Retrain Model" button
3. Wait for training to complete (you'll see a success message)

## Step 5: Take Attendance

**Method 1 - Using Webcam:**
1. Click "Start Camera"
2. Position students in frame
3. Click "Capture & Mark Attendance"

**Method 2 - Upload Photo:**
1. Click "Upload Class Photo"
2. Select a photo from your computer
3. System will automatically recognize faces

## Step 6: View Attendance

1. Click on "View Attendance" tab
2. Click "Today's Attendance" or "All Records"

## Tips

- Use good lighting for better recognition
- Ensure faces are clearly visible
- The system works best with 3-5 photos per student
- Retrain the model whenever you add new students

## Troubleshooting

**Camera doesn't work:**
- Check browser permissions
- Make sure camera isn't being used by another app

**Poor recognition:**
- Add more photos per student
- Ensure photos are clear and well-lit
- Try adjusting the recognition threshold in app.py

**Installation errors:**
- Make sure Python 3.8+ is installed
- For dlib issues, try: `pip install cmake` first
- On Windows, you may need Visual Studio Build Tools
