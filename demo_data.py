"""
Demo Data Generator for Smart Attendance App
Run this to populate your database with sample data for testing.

Usage:
    python demo_data.py
"""

import requests
import json
from datetime import datetime, timedelta
import random

BASE_URL = "http://localhost:5000"

def add_student(name, roll, email, phone, class_id, subjects):
    data = {
        'name': name,
        'roll_number': roll,
        'email': email,
        'phone': phone,
        'class_id': class_id,
        'subjects': subjects
    }
    try:
        r = requests.post(f"{BASE_URL}/admin/add_student", data=data)
        print(f"Added student: {name}")
    except Exception as e:
        print(f"Error adding {name}: {e}")

def add_teacher(name, email, phone, subjects, assigned_classes, password):
    data = {
        'name': name,
        'email': email,
        'phone': phone,
        'subjects': subjects,
        'assigned_classes': assigned_classes,
        'password': password
    }
    try:
        r = requests.post(f"{BASE_URL}/admin/add_teacher", data=data)
        print(f"Added teacher: {name}")
    except Exception as e:
        print(f"Error adding {name}: {e}")

def add_class(class_name, department, subjects):
    data = {
        'class_name': class_name,
        'department': department,
        'subjects': subjects
    }
    try:
        r = requests.post(f"{BASE_URL}/admin/add_class", data=data)
        print(f"Added class: {class_name}")
    except Exception as e:
        print(f"Error adding {class_name}: {e}")

if __name__ == '__main__':
    print("Generating demo data...")
    print("Make sure the app is running on localhost:5000")
    print("=" * 50)

    # Add classes
    add_class("BSc Computer Science FY", "Computer Science", 
              "Mathematics, Physics, Computer Fundamentals, C Programming")
    add_class("BSc Computer Science SY", "Computer Science", 
              "Data Structures, Database Management, Operating Systems, Web Development")
    add_class("BCom FY", "Commerce", 
              "Accountancy, Economics, Business Law, Statistics")

    print("\nDemo data generation complete!")
    print("Login with: admin@school.com / admin123")
