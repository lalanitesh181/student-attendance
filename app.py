"""
Smart Attendance App - Flask Backend with Firebase
Run: python app.py
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from functools import wraps
import firebase_admin
from firebase_admin import credentials, firestore, auth
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# ------------------------------------------------------------------
# FIREBASE INITIALIZATION
# ------------------------------------------------------------------
# Option 1: Using service account JSON file (for local development)
# Download your serviceAccountKey.json from Firebase Console > Project Settings > Service Accounts
SERVICE_ACCOUNT_PATH = 'firebase_service_account.json'

# Option 2: Using environment variable (for deployment)
# Set FIREBASE_CONFIG env variable with the JSON content

def init_firebase():
    try:
        if os.path.exists(SERVICE_ACCOUNT_PATH):
            cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
        else:
            # Fallback: try environment variable
            firebase_config = os.environ.get('FIREBASE_CONFIG')
            if firebase_config:
                cred = credentials.Certificate(json.loads(firebase_config))
            else:
                print("WARNING: No Firebase credentials found. Using dummy mode.")
                return None

        firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception as e:
        print(f"Firebase init error: {e}")
        return None

db = init_firebase()

# ------------------------------------------------------------------
# MOCK DATABASE (Fallback if Firebase is not configured)
# ------------------------------------------------------------------
MOCK_STUDENTS = []
MOCK_TEACHERS = []
MOCK_CLASSES = []
MOCK_ATTENDANCE = []

# ------------------------------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------------------------------
def get_collection_ref(collection_name):
    if db:
        return db.collection(collection_name)
    return None

def add_document(collection, data):
    if db:
        doc_ref = db.collection(collection).document()
        data['id'] = doc_ref.id
        doc_ref.set(data)
        return doc_ref.id
    else:
        # Mock mode
        data['id'] = str(datetime.now().timestamp())
        if collection == 'students':
            MOCK_STUDENTS.append(data)
        elif collection == 'teachers':
            MOCK_TEACHERS.append(data)
        elif collection == 'classes':
            MOCK_CLASSES.append(data)
        elif collection == 'attendance':
            MOCK_ATTENDANCE.append(data)
        return data['id']

def get_all_documents(collection):
    if db:
        docs = db.collection(collection).stream()
        return [{**doc.to_dict(), 'id': doc.id} for doc in docs]
    else:
        if collection == 'students':
            return MOCK_STUDENTS
        elif collection == 'teachers':
            return MOCK_TEACHERS
        elif collection == 'classes':
            return MOCK_CLASSES
        elif collection == 'attendance':
            return MOCK_ATTENDANCE
        return []

def get_document_by_field(collection, field, value):
    docs = get_all_documents(collection)
    return [d for d in docs if d.get(field) == value]

# ------------------------------------------------------------------
# LOGIN DECORATOR
# ------------------------------------------------------------------
def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please login first', 'warning')
                return redirect(url_for('login'))
            if role and session.get('role') != role and session.get('role') != 'admin':
                flash('Unauthorized access', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ------------------------------------------------------------------
# ROUTES
# ------------------------------------------------------------------

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        # Simple demo authentication
        # In production, use Firebase Auth or hashed passwords
        users = get_all_documents('users')
        user = None
        for u in users:
            if u.get('email') == email and u.get('password') == password:
                user = u
                break

        # Demo accounts (create if not exists)
        demo_accounts = {
            'admin@school.com': {'password': 'admin123', 'role': 'admin', 'name': 'Administrator'},
            'teacher@school.com': {'password': 'teacher123', 'role': 'teacher', 'name': 'Demo Teacher'}
        }

        if not user and email in demo_accounts:
            demo = demo_accounts[email]
            if password == demo['password']:
                user = {
                    'email': email,
                    'role': demo['role'],
                    'name': demo['name'],
                    'id': email
                }
        elif not user:
            flash('Invalid credentials', 'danger')
            return render_template('login.html')

        if user:
            session['user_id'] = user.get('id', email)
            session['email'] = email
            session['role'] = user.get('role', role)
            session['name'] = user.get('name', 'User')
            flash(f'Welcome, {session["name"]}!', 'success')
            return redirect(url_for('dashboard'))

        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required()
def dashboard():
    if session.get('role') == 'admin':
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('teacher_dashboard'))

# ===================== ADMIN ROUTES =====================

@app.route('/admin')
@login_required(role='admin')
def admin_dashboard():
    students = get_all_documents('students')
    teachers = get_all_documents('teachers')
    classes = get_all_documents('classes')
    return render_template('admin_dashboard.html', 
                         students=students, 
                         teachers=teachers, 
                         classes=classes,
                         total_students=len(students),
                         total_teachers=len(teachers),
                         total_classes=len(classes))

@app.route('/admin/add_student', methods=['POST'])
@login_required(role='admin')
def add_student():
    data = {
        'name': request.form.get('name'),
        'roll_number': request.form.get('roll_number'),
        'email': request.form.get('email'),
        'phone': request.form.get('phone'),
        'class_id': request.form.get('class_id'),
        'subjects': request.form.getlist('subjects'),
        'created_at': datetime.now().isoformat()
    }
    add_document('students', data)
    flash('Student added successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/add_teacher', methods=['POST'])
@login_required(role='admin')
def add_teacher():
    data = {
        'name': request.form.get('name'),
        'email': request.form.get('email'),
        'phone': request.form.get('phone'),
        'subjects': request.form.getlist('subjects'),
        'assigned_classes': request.form.getlist('assigned_classes'),
        'password': request.form.get('password'),  # In production, hash this!
        'role': 'teacher',
        'created_at': datetime.now().isoformat()
    }
    add_document('teachers', data)
    # Also add to users collection for login
    add_document('users', {
        'email': data['email'],
        'password': data['password'],
        'role': 'teacher',
        'name': data['name']
    })
    flash('Teacher added successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/add_class', methods=['POST'])
@login_required(role='admin')
def add_class():
    data = {
        'class_name': request.form.get('class_name'),
        'department': request.form.get('department'),
        'subjects': [{'name': s.strip(), 'code': s.strip().replace(" ", "_").lower()} 
                     for s in request.form.get('subjects').split(',')],
        'created_at': datetime.now().isoformat()
    }
    add_document('classes', data)
    flash('Class added successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# ===================== TEACHER ROUTES =====================

@app.route('/teacher')
@login_required(role='teacher')
def teacher_dashboard():
    teacher_email = session.get('email')
    teachers = get_all_documents('teachers')
    teacher = None
    for t in teachers:
        if t.get('email') == teacher_email:
            teacher = t
            break

    classes = get_all_documents('classes')
    attendance = get_all_documents('attendance')

    # Filter attendance by this teacher
    if teacher:
        teacher_attendance = [a for a in attendance if a.get('teacher_id') == teacher.get('id')]
    else:
        teacher_attendance = attendance[:10]  # Show recent

    return render_template('teacher_dashboard.html',
                         teacher=teacher,
                         classes=classes,
                         attendance=teacher_attendance)

@app.route('/teacher/mark_attendance', methods=['GET', 'POST'])
@login_required(role='teacher')
def mark_attendance():
    if request.method == 'POST':
        class_id = request.form.get('class_id')
        subject = request.form.get('subject')
        date_str = request.form.get('date')
        teacher_id = session.get('user_id')

        students = get_all_documents('students')
        class_students = [s for s in students if s.get('class_id') == class_id]

        attendance_records = {}
        for student in class_students:
            status = request.form.get(f'student_{student["id"]}', 'absent')
            attendance_records[student['id']] = {
                'name': student['name'],
                'roll_number': student.get('roll_number', ''),
                'status': status
            }

        data = {
            'class_id': class_id,
            'subject': subject,
            'date': date_str,
            'teacher_id': teacher_id,
            'teacher_name': session.get('name'),
            'records': attendance_records,
            'created_at': datetime.now().isoformat()
        }

        # Check if attendance already exists for this date/class/subject
        existing = get_all_documents('attendance')
        updated = False
        for att in existing:
            if (att.get('class_id') == class_id and 
                att.get('subject') == subject and 
                att.get('date') == date_str):
                # Update existing
                if db:
                    db.collection('attendance').document(att['id']).update({'records': attendance_records})
                else:
                    att['records'] = attendance_records
                updated = True
                break

        if not updated:
            add_document('attendance', data)

        flash('Attendance saved successfully!', 'success')
        return redirect(url_for('teacher_dashboard'))

    # GET request
    class_id = request.args.get('class_id', '')
    subject = request.args.get('subject', '')
    date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))

    classes = get_all_documents('classes')
    students = get_all_documents('students')
    class_students = [s for s in students if s.get('class_id') == class_id]

    # Load existing attendance if any
    existing_records = {}
    if class_id and subject and date_str:
        attendance = get_all_documents('attendance')
        for att in attendance:
            if (att.get('class_id') == class_id and 
                att.get('subject') == subject and 
                att.get('date') == date_str):
                existing_records = att.get('records', {})
                break

    return render_template('mark_attendance.html',
                         classes=classes,
                         students=class_students,
                         selected_class=class_id,
                         selected_subject=subject,
                         selected_date=date_str,
                         existing_records=existing_records)

@app.route('/teacher/view_attendance')
@login_required(role='teacher')
def view_attendance():
    class_id = request.args.get('class_id', '')
    subject = request.args.get('subject', '')

    attendance = get_all_documents('attendance')
    classes = get_all_documents('classes')

    filtered = [a for a in attendance if 
                (not class_id or a.get('class_id') == class_id) and
                (not subject or a.get('subject') == subject)]

    return render_template('view_attendance.html',
                         attendance=filtered,
                         classes=classes,
                         selected_class=class_id,
                         selected_subject=subject)

# ===================== API ROUTES (for mobile app) =====================

@app.route('/api/students')
def api_students():
    class_id = request.args.get('class_id')
    students = get_all_documents('students')
    if class_id:
        students = [s for s in students if s.get('class_id') == class_id]
    return jsonify(students)

@app.route('/api/classes')
def api_classes():
    return jsonify(get_all_documents('classes'))

@app.route('/api/attendance', methods=['POST'])
def api_post_attendance():
    data = request.json
    data['created_at'] = datetime.now().isoformat()
    doc_id = add_document('attendance', data)
    return jsonify({'success': True, 'id': doc_id})

@app.route('/api/attendance')
def api_get_attendance():
    class_id = request.args.get('class_id')
    date_str = request.args.get('date')
    attendance = get_all_documents('attendance')

    if class_id:
        attendance = [a for a in attendance if a.get('class_id') == class_id]
    if date_str:
        attendance = [a for a in attendance if a.get('date') == date_str]

    return jsonify(attendance)

# ------------------------------------------------------------------
# INIT DEMO DATA
# ------------------------------------------------------------------
@app.before_request
def init_demo_data():
    # Only run once - check if users collection has admin
    if not hasattr(app, '_demo_initialized'):
        app._demo_initialized = True
        users = get_all_documents('users')
        if not users:
            # Create admin user
            add_document('users', {
                'email': 'admin@school.com',
                'password': 'admin123',
                'role': 'admin',
                'name': 'Administrator'
            })
            print("Demo admin created: admin@school.com / admin123")
            print("Demo teacher: teacher@school.com / teacher123")

if __name__ == '__main__':
    print("=" * 60)
    print("Smart Attendance App Starting...")
    print("Admin Login: admin@school.com / admin123")
    print("Teacher Login: teacher@school.com / teacher123")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)
