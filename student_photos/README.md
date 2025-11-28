# Instructions for Setting Up Student Photos

This directory should contain folders for each student, with each folder containing photos of that student.

## Directory Structure

```
student_photos/
├── Student_001/
│   ├── photo1.jpg
│   ├── photo2.jpg
│   └── photo3.jpg
├── Student_002/
│   ├── photo1.jpg
│   └── photo2.jpg
└── Student_003/
    ├── photo1.jpg
    ├── photo2.jpg
    └── photo3.jpg
```

## Guidelines for Student Photos

1. **Folder Names**: Use student IDs or names (e.g., Student_001, John_Doe, etc.)
   - Folder name will be used as the student identifier in attendance records

2. **Number of Photos**: Add 3-5 photos per student
   - More photos = better recognition accuracy
   - Photos should show different expressions and slight angle variations

3. **Photo Quality**:
   - Clear, front-facing photos
   - Good lighting (avoid shadows on face)
   - Avoid sunglasses or face coverings
   - Resolution: At least 640x480 pixels
   - Supported formats: .jpg, .jpeg, .png

4. **Photo Capture Tips**:
   - Face should be clearly visible
   - Neutral to slight smile expressions
   - Eyes open and looking at camera
   - Similar to passport photo style
   - Include slight variations (small head tilts, different expressions)

## Example for 10 Students

Create 10 folders named:
- Student_001
- Student_002
- Student_003
- Student_004
- Student_005
- Student_006
- Student_007
- Student_008
- Student_009
- Student_010

Add 3-5 photos in each folder.

## After Adding Photos

1. Go to the web application (http://localhost:5000)
2. Click on "Train/Retrain Model" button
3. Wait for the training to complete
4. You can now start taking attendance!

## Notes

- The first time you run the application, it will automatically train the model if photos are present
- Whenever you add new students, remember to retrain the model
- You can add more than 10 students by creating additional folders
