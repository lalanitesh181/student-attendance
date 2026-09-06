# Smart Attendance App - Flask + Firebase

A complete web-based attendance management system with Admin and Teacher interfaces, built with Python Flask and Firebase Firestore. Works perfectly on mobile phones!

## Features

### Admin Interface
- Add and manage students with roll numbers, emails, phone numbers
- Add teachers with assigned subjects and classes
- Create classes with subjects list
- View all data in organized tables
- Search functionality built-in

### Teacher Interface
- Mark attendance with simple Present/Absent toggle buttons
- Select class, subject, and date before marking
- Mark all present/absent with one click
- View attendance history with statistics
- Mobile-optimized for easy phone use

### Technical Features
- Responsive design (works on mobile, tablet, desktop)
- Real-time data with Firebase Firestore
- REST API endpoints for mobile app integration
- Demo mode works without Firebase (in-memory storage)
- Flash messages for user feedback

## Project Structure

```
attendance_app/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── firebase_service_account.json # Firebase credentials (you add this)
├── README.md                   # This file
├── templates/
│   ├── base.html              # Base layout
│   ├── login.html             # Login page
│   ├── admin_dashboard.html   # Admin panel
│   ├── teacher_dashboard.html # Teacher home
│   ├── mark_attendance.html   # Attendance marking
│   └── view_attendance.html   # Attendance reports
└── static/
    ├── css/
    │   └── style.css          # Mobile-responsive styles
    └── js/
        └── app.js              # Interactive features
```

## Setup Instructions

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Set Up Firebase (Optional but Recommended)

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project
3. Go to Project Settings > Service Accounts
4. Click "Generate new private key"
5. Save the downloaded file as `firebase_service_account.json` in the project folder

If you skip this step, the app will run in demo mode with in-memory storage.

### Step 3: Run the Application

```bash
python app.py
```

Open your browser and go to: `http://localhost:5000`

## Demo Login Credentials

| Role  | Email                | Password    |
|-------|----------------------|-------------|
| Admin | admin@school.com     | admin123    |
| Teacher | teacher@school.com | teacher123  |

## Using on Mobile Phone

### Option 1: Same WiFi Network
1. Find your computer's IP address (run `ipconfig` on Windows or `ifconfig` on Mac/Linux)
2. On your phone browser, open: `http://YOUR_COMPUTER_IP:5000`
3. Both devices must be on the same WiFi

### Option 2: Deploy Online (Free)
See the deployment section below.

## API Endpoints (for Mobile App)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/students` | GET | Get all students (optionally filter by `class_id`) |
| `/api/classes` | GET | Get all classes and subjects |
| `/api/attendance` | GET | Get attendance records (filter by `class_id` or `date`) |
| `/api/attendance` | POST | Submit attendance data |

### Example: POST Attendance
```json
{
  "class_id": "class123",
  "subject": "Mathematics",
  "date": "2025-01-15",
  "teacher_id": "teacher456",
  "teacher_name": "John Doe",
  "records": {
    "student1": {"name": "Alice", "roll_number": "101", "status": "present"},
    "student2": {"name": "Bob", "roll_number": "102", "status": "absent"}
  }
}
```

## Free Deployment Options

### Option 1: Render (Recommended)
1. Push code to GitHub
2. Go to [render.com](https://render.com) and sign up
3. Create a new Web Service, connect your GitHub repo
4. Set environment variables:
   - `FIREBASE_CONFIG`: Paste contents of your serviceAccountKey.json
5. Build command: `pip install -r requirements.txt`
6. Start command: `gunicorn app:app`
7. Add `gunicorn` to requirements.txt

### Option 2: PythonAnywhere
1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload files via Files tab
3. Install requirements
4. Configure WSGI file to point to your app

### Option 3: Railway
1. Push code to GitHub
2. Go to [railway.app](https://railway.app)
3. New project from GitHub repo
4. Add `FIREBASE_CONFIG` environment variable

## Next Steps for Your Aavishkaar Project

1. **Add Firebase**: Connect real database for live demo
2. **Add Student Interface**: Create student login to view attendance
3. **Add Messages/Notices**: Implement the messaging feature
4. **Add QR Attendance**: Generate QR codes for quick marking
5. **Deploy Online**: Host on Render or PythonAnywhere for presentation

## For Aavishkaar Poster

Use these technical details in your poster:
- **Backend**: Python Flask
- **Database**: Firebase Firestore (NoSQL)
- **Frontend**: HTML5, CSS3, JavaScript
- **Mobile**: Responsive design with CSS Grid and Flexbox
- **API**: RESTful JSON API for future mobile app expansion
- **Hosting**: Can be deployed on Render, Railway, or PythonAnywhere for free

## Team

This project was built for Aavishkaar 2026-2027, Savitribai Phule Pune University.
