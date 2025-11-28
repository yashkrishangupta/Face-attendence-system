import os
import cv2
import numpy as np
import pickle
import json
import base64
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from deepface import DeepFace

app = Flask(__name__)

# Configuration
STUDENT_PHOTOS_DIR = 'student_photos'
ATTENDANCE_DIR = 'attendance_records'
ENCODINGS_FILE = 'face_encodings.pkl'

# DeepFace settings - using VGG-Face model for accuracy
FACE_MODEL = 'VGG-Face'  # Accurate and reliable
DISTANCE_METRIC = 'cosine'
RECOGNITION_THRESHOLD = 0.4  # Lower = stricter

# Ensure directories exist
os.makedirs(STUDENT_PHOTOS_DIR, exist_ok=True)
os.makedirs(ATTENDANCE_DIR, exist_ok=True)

# Global variables
student_embeddings = {}  # {student_name: [embeddings]}
face_cascade = None


def init_face_cascade():
    """Initialize Haar Cascade"""
    global face_cascade
    if face_cascade is None:
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    return face_cascade


def load_student_photos():
    """Load student photos and create DeepFace embeddings"""
    global student_embeddings
    
    student_embeddings = {}
    
    if not os.path.isdir(STUDENT_PHOTOS_DIR):
        return False
    
    print(f"\n📸 Loading student photos with DeepFace ({FACE_MODEL})...")
    print("   (Using deep neural network for high accuracy)\n")
    
    for student_folder in sorted(os.listdir(STUDENT_PHOTOS_DIR)):
        student_path = os.path.join(STUDENT_PHOTOS_DIR, student_folder)
        if not os.path.isdir(student_path):
            continue
        
        embeddings = []
        
        for photo_file in os.listdir(student_path):
            if not photo_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
            
            photo_path = os.path.join(student_path, photo_file)
            
            try:
                # Create embedding using DeepFace
                embedding_objs = DeepFace.represent(
                    img_path=photo_path,
                    model_name=FACE_MODEL,
                    enforce_detection=True,
                    detector_backend='opencv'
                )
                
                if embedding_objs and len(embedding_objs) > 0:
                    # Get the embedding (first face found)
                    embedding = embedding_objs[0]['embedding']
                    embeddings.append(embedding)
                    
            except Exception as e:
                # Skip photos with no faces or errors
                continue
        
        if len(embeddings) > 0:
            student_embeddings[student_folder] = embeddings
            print(f"  ✓ {student_folder}: {len(embeddings)} photos encoded")
    
    print(f"\n✅ Created embeddings for {len(student_embeddings)} students!\n")
    return len(student_embeddings) > 0


def train_model():
    """Train model by creating face embeddings"""
    try:
        success = load_student_photos()
        
        if not success:
            print("❌ No student data found")
            return False
        
        # Save embeddings
        with open(ENCODINGS_FILE, 'wb') as f:
            pickle.dump(student_embeddings, f)
        
        print(f"💾 Saved embeddings for {len(student_embeddings)} students\n")
        return True
        
    except Exception as e:
        print(f"❌ Error training: {e}")
        import traceback
        traceback.print_exc()
        return False


def load_model():
    """Load face embeddings"""
    global student_embeddings
    
    try:
        if os.path.exists(ENCODINGS_FILE):
            with open(ENCODINGS_FILE, 'rb') as f:
                student_embeddings = pickle.load(f)
            
            print(f"✅ Loaded embeddings for {len(student_embeddings)} students")
            return True
        else:
            print("⚠️  Embeddings not found. Please train first.")
            return False
            
    except Exception as e:
        print(f"❌ Error loading embeddings: {e}")
        return False


def cosine_distance(embedding1, embedding2):
    """Calculate cosine distance between two embeddings"""
    embedding1 = np.array(embedding1)
    embedding2 = np.array(embedding2)
    
    # Normalize
    embedding1_norm = embedding1 / np.linalg.norm(embedding1)
    embedding2_norm = embedding2 / np.linalg.norm(embedding2)
    
    # Cosine similarity
    similarity = np.dot(embedding1_norm, embedding2_norm)
    
    # Convert to distance (0 = same, 1 = different)
    distance = 1 - similarity
    
    return distance


def recognize_faces(image_array):
    """Recognize faces using DeepFace embeddings"""
    global student_embeddings
    
    if len(student_embeddings) == 0:
        load_model()
    
    if len(student_embeddings) == 0:
        return {'recognized': [], 'unknown': []}
    
    recognized_students = []
    unknown_faces = []
    
    # Convert RGB to BGR for OpenCV
    bgr_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
    
    # Detect faces using Haar Cascade (faster)
    cascade = init_face_cascade()
    gray = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
    detected_faces = cascade.detectMultiScale(
        gray, 
        scaleFactor=1.1, 
        minNeighbors=5, 
        minSize=(50, 50)
    )
    
    print(f"\n🔍 Detected {len(detected_faces)} face(s)")
    
    for (x, y, w, h) in detected_faces:
        # Extract face region
        face_img = bgr_image[y:y+h, x:x+w]
        
        try:
            # Create embedding for this face
            face_embedding_objs = DeepFace.represent(
                img_path=face_img,
                model_name=FACE_MODEL,
                enforce_detection=False,  # We already detected the face
                detector_backend='skip'
            )
            
            if not face_embedding_objs or len(face_embedding_objs) == 0:
                continue
            
            face_embedding = face_embedding_objs[0]['embedding']
            
            # Compare with all students
            best_match = None
            best_distance = float('inf')
            
            for student_name, embeddings_list in student_embeddings.items():
                for stored_embedding in embeddings_list:
                    # Calculate distance
                    distance = cosine_distance(face_embedding, stored_embedding)
                    
                    if distance < best_distance:
                        best_distance = distance
                        best_match = student_name
            
            print(f"   Best match: {best_match}, Distance: {best_distance:.3f}, Threshold: {RECOGNITION_THRESHOLD}")
            
            if best_distance < RECOGNITION_THRESHOLD:
                # Recognized!
                confidence = 1.0 - best_distance
                
                print(f"   ✅ RECOGNIZED: {best_match} (confidence: {confidence:.2%})")
                
                recognized_students.append({
                    'student_id': best_match,
                    'confidence': float(confidence),
                    'raw_confidence': float(best_distance),
                    'location': {
                        'top': int(y),
                        'right': int(x + w),
                        'bottom': int(y + h),
                        'left': int(x)
                    }
                })
            else:
                # Unknown
                print(f"   ❌ UNKNOWN (distance: {best_distance:.3f} > threshold: {RECOGNITION_THRESHOLD})")
                
                unknown_faces.append({
                    'location': {
                        'top': int(y),
                        'right': int(x + w),
                        'bottom': int(y + h),
                        'left': int(x)
                    },
                    'confidence': float(best_distance)
                })
                
        except Exception as e:
            print(f"   ⚠️  Error processing face: {e}")
            continue
    
    return {'recognized': recognized_students, 'unknown': unknown_faces}


def mark_attendance(student_ids):
    """Mark attendance"""
    today = datetime.now().strftime('%Y-%m-%d')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    attendance_file = os.path.join(ATTENDANCE_DIR, f'{today}.json')
    
    if os.path.exists(attendance_file):
        with open(attendance_file, 'r') as f:
            attendance_data = json.load(f)
    else:
        attendance_data = {
            'date': today,
            'records': {}
        }
    
    for student_id in student_ids:
        if student_id not in attendance_data['records']:
            attendance_data['records'][student_id] = {
                'status': 'Present',
                'timestamp': timestamp
            }
    
    with open(attendance_file, 'w') as f:
        json.dump(attendance_data, f, indent=4)
    
    return attendance_data


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/attendance')
def attendance_page():
    return render_template('attendance.html')


@app.route('/train', methods=['POST'])
def train():
    """Train endpoint"""
    try:
        success = train_model()
        if success:
            return jsonify({'success': True, 'message': f'Created embeddings for {len(student_embeddings)} students using {FACE_MODEL}'})
        else:
            return jsonify({'success': False, 'message': 'No student data'})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)})


@app.route('/recognize', methods=['POST'])
def recognize():
    """Recognize endpoint"""
    try:
        data = request.get_json()
        
        if 'image' not in data:
            return jsonify({'success': False, 'message': 'No image'})
        
        # Decode image
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Flip for mirror view
        image = cv2.flip(image, 1)
        
        # Convert to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Recognize
        result = recognize_faces(rgb_image)
        recognized = result['recognized']
        unknown = result['unknown']
        
        response_data = {
            'success': True,
            'recognized_students': recognized,
            'unknown_persons': unknown,
            'message': f'Found {len(recognized)} student(s)'
        }
        
        if recognized:
            student_ids = [s['student_id'] for s in recognized]
            attendance_data = mark_attendance(student_ids)
            response_data['attendance'] = attendance_data
        
        if unknown:
            response_data['message'] += f' and {len(unknown)} unknown'
            response_data['alert'] = True
        
        return jsonify(response_data)
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'success': False, 'message': str(e)})


@app.route('/attendance/today', methods=['GET'])
def get_today_attendance():
    """Get today's attendance"""
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        attendance_file = os.path.join(ATTENDANCE_DIR, f'{today}.json')
        
        if os.path.exists(attendance_file):
            with open(attendance_file, 'r') as f:
                attendance_data = json.load(f)
            return jsonify({'success': True, 'data': attendance_data})
        else:
            return jsonify({'success': True, 'data': {'date': today, 'records': {}}})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/attendance/all', methods=['GET'])
def get_all_attendance():
    """Get all attendance"""
    try:
        all_records = []
        
        for filename in os.listdir(ATTENDANCE_DIR):
            if filename.endswith('.json'):
                file_path = os.path.join(ATTENDANCE_DIR, filename)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    all_records.append(data)
        
        all_records.sort(key=lambda x: x['date'], reverse=True)
        
        return jsonify({'success': True, 'data': all_records})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/students', methods=['GET'])
def get_students():
    """Get students list"""
    try:
        students = []
        for student_folder in os.listdir(STUDENT_PHOTOS_DIR):
            student_path = os.path.join(STUDENT_PHOTOS_DIR, student_folder)
            if os.path.isdir(student_path):
                students.append(student_folder)
        
        students.sort()
        return jsonify({'success': True, 'students': students})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


if __name__ == '__main__':
    print("\n🚀 Starting Face Attendance System...\n")
    load_model()
    app.run(debug=True, host='0.0.0.0', port=5000)
