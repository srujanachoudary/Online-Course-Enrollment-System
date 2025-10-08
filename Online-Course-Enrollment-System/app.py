# app.py
import streamlit as st
from src.dao.student_dao import StudentDAO
from src.dao.course_dao import CourseDAO
from src.dao.enrollment_dao import EnrollmentDAO
from src.dao.payment_dao import PaymentDAO

from src.services.student_service import StudentService
from src.services.enrollment_service import EnrollmentService
from src.services.payment_service import PaymentService
from src.services.admin_service import AdminService

# Initialize DAOs
student_dao = StudentDAO()
course_dao = CourseDAO()
enrollment_dao = EnrollmentDAO()
payment_dao = PaymentDAO()

# Initialize Services
student_service = StudentService(student_dao)
enrollment_service = EnrollmentService(enrollment_dao)
payment_service = PaymentService(payment_dao, enrollment_dao)
admin_service = AdminService(course_dao, enrollment_dao, payment_dao)

# --- Streamlit App ---
st.title("University Course Management System")

# Sidebar: Login/Register or Admin
menu = st.sidebar.selectbox("Menu", ["Home", "Student Register/Login", "Admin Panel"])

if menu == "Home":
    st.subheader("Welcome to University Course Management System")
    st.write("Use the sidebar to navigate.")

# ------------------ Student Section ------------------
if menu == "Student Register/Login":
    action = st.selectbox("Action", ["Register", "Login"])

    if action == "Register":
        st.subheader("Student Registration")
        name = st.text_input("Name")
        email = st.text_input("Email")
        department = st.text_input("Department")
        phone = st.text_input("Phone")

        if st.button("Register"):
            existing = student_dao.get_student_by_email(email)
            if existing:
                st.warning("Email already registered. Please login.")
            else:
                student_id = student_dao.add_student(name, email, department, phone)
                if student_id:
                    st.success(f"Registered successfully! Your student ID: {student_id}")
                else:
                    st.error("Registration failed.")

    elif action == "Login":
        st.subheader("Student Login")
        email = st.text_input("Email", key="login_email")
        if st.button("Login"):
            student = student_dao.get_student_by_email(email)
            if student:
                st.session_state["student"] = student
                st.success(f"Welcome, {student.get('name')}!")
            else:
                st.error("No student found with this email.")

    # If logged in, show student dashboard
    if "student" in st.session_state:
        student = st.session_state["student"]
        st.subheader("Student Dashboard")
        st.write(f"Logged in as: {student.get('name')} ({student.get('email')})")

        student_courses = st.selectbox("Action", ["Enroll in Course", "View My Enrollments", "Pay for Enrollment"])
        
        # Enroll in a course
        if student_courses == "Enroll in Course":
            courses = course_dao.get_all_courses()
            course_options = {c["title"]: c["course_id"] for c in courses}
            selected_course = st.selectbox("Select Course", list(course_options.keys()))
            if st.button("Enroll"):
                enrollment_service.enroll_course(student.get("student_id"), course_options[selected_course])
        
        # View enrollments
        elif student_courses == "View My Enrollments":
            enrollments = enrollment_dao.get_enrollments_by_student(student.get("student_id"))
            if not enrollments:
                st.info("No enrollments found.")
            else:
                for e in enrollments:
                    st.write(f"Enrollment ID: {e.get('enrollment_id')}, Course ID: {e.get('course_id')}, Status: {e.get('status','N/A')}")
                    if st.button(f"Drop {e.get('enrollment_id')}", key=e.get('enrollment_id')):
                        enrollment_service.drop_course(e.get('enrollment_id'))
        
        # Pay for enrollment
        elif student_courses == "Pay for Enrollment":
            enrollments = enrollment_dao.get_enrollments_by_student(student.get("student_id"))
            pending_enrollments = [e for e in enrollments if e.get("status") != "Paid"]
            if not pending_enrollments:
                st.info("No pending payments.")
            else:
                selected_enroll = st.selectbox("Select Enrollment to Pay", [e["enrollment_id"] for e in pending_enrollments])
                amount = st.number_input("Amount", min_value=0.0, step=0.01)
                if st.button("Pay"):
                    payment_service.pay_for_enrollment(selected_enroll, amount)

# ------------------ Admin Section ------------------
elif menu == "Admin Panel":
    st.subheader("Admin Panel")
    admin_actions = st.selectbox("Action", ["Add Course", "Edit Course", "Delete Course", "View Enrollments", "Generate Reports"])
    
    if admin_actions == "Add Course":
        title = st.text_input("Course Title")
        credits = st.number_input("Credits", min_value=0)
        faculty = st.text_input("Faculty")
        if st.button("Add Course"):
            course_id = course_dao.add_course(title, credits, faculty)
            if course_id:
                st.success(f"Course added! ID: {course_id}")
            else:
                st.error("Failed to add course.")
    
    elif admin_actions == "Edit Course":
        courses = course_dao.get_all_courses()
        course_options = {c["title"]: c["course_id"] for c in courses}
        selected_course = st.selectbox("Select Course to Edit", list(course_options.keys()))
        new_title = st.text_input("New Title (leave blank to skip)")
        new_credits = st.number_input("New Credits (0 to skip)", min_value=0, step=1)
        new_faculty = st.text_input("New Faculty (leave blank to skip)")
        if st.button("Update Course"):
            success = course_dao.edit_course(
                course_options[selected_course],
                new_title or None,
                new_credits if new_credits > 0 else None,
                new_faculty or None
            )
            st.success("Course updated." if success else "Failed to update course.")

    elif admin_actions == "Delete Course":
        courses = course_dao.get_all_courses()
        course_options = {c["title"]: c["course_id"] for c in courses}
        selected_course = st.selectbox("Select Course to Delete", list(course_options.keys()))
        if st.button("Delete Course"):
            success = course_dao.delete_course(course_options[selected_course])
            st.success("Course deleted." if success else "Failed to delete course.")

    elif admin_actions == "View Enrollments":
        enrollments = enrollment_dao.get_all_enrollments()
        if not enrollments:
            st.info("No enrollments.")
        else:
            for e in enrollments:
                st.write(f"Enrollment ID: {e.get('enrollment_id')}, Student: {e.get('student_id')}, Course: {e.get('course_id')}, Status: {e.get('status','N/A')}")

    elif admin_actions == "Generate Reports":
        courses = course_dao.get_all_courses()
        enrollments = enrollment_dao.get_all_enrollments()
        st.write("--- Enrollment Counts per Course ---")
        for c in courses:
            cid = c.get("course_id")
            count = sum(1 for e in enrollments if e.get("course_id") == cid)
            st.write(f"{c.get('title')} (ID {cid}) -> {count} students")
        payments = payment_dao.get_all_payments()
        total_amount = sum(float(p.get("amount", 0)) for p in payments)
        st.write(f"\nTotal Payments: {len(payments)}, Total Amount: {total_amount}")
