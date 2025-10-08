# src/services/student_service.py
from typing import Optional

class StudentService:
    def __init__(self, student_dao):
        self.student_dao = student_dao
        self.current_student: Optional[dict] = None

    def register_student(self):
        print("\n--- Student Registration ---")
        name = input("Enter your name: ").strip()
        email = input("Enter your email: ").strip()
        department = input("Enter your department: ").strip()
        phone = input("Enter your phone number: ").strip()

        existing = self.student_dao.get_student_by_email(email)
        if existing:
            print("Email already registered. Please login.")
            return

        student_id = self.student_dao.add_student(name, email, department, phone)
        if student_id:
            print(f"Registration successful! Your student ID: {student_id}")
        else:
            print("Registration failed. Try again later.")

    def login_student(self):
        print("\n--- Student Login ---")
        email = input("Enter your email: ").strip()
        student = self.student_dao.get_student_by_email(email)
        if not student:
            print("No student found with this email.")
            return
        self.current_student = student
        print(f"Welcome, {student.get('name')}!")

    def view_student_details(self):
        if not self.current_student:
            print("No student logged in. Please login first.")
            return
        s = self.current_student
        print("\n--- Student Details ---")
        print(f"ID        : {s.get('student_id')}")
        print(f"Name      : {s.get('name')}")
        print(f"Email     : {s.get('email')}")
        print(f"Department: {s.get('department')}")
        print(f"Phone     : {s.get('phone')}")

    def logout_student(self):
        if self.current_student:
            print(f"Student {self.current_student.get('name')} logged out.")
            self.current_student = None
        else:
            print("No student is currently logged in.")
