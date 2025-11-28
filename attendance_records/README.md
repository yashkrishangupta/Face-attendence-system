# Attendance Records

This directory stores daily attendance records in JSON format.

## File Format

Each day's attendance is stored in a separate JSON file named with the date: `YYYY-MM-DD.json`

Example: `2025-11-27.json`

## JSON Structure

```json
{
    "date": "2025-11-27",
    "records": {
        "Student_001": {
            "status": "Present",
            "timestamp": "2025-11-27 09:15:30"
        },
        "Student_002": {
            "status": "Present",
            "timestamp": "2025-11-27 09:15:30"
        }
    }
}
```

## Notes

- Files are automatically created when attendance is marked
- Each student is recorded only once per day (first recognition)
- Timestamps show when the student was first detected
- You can view these records through the web interface
