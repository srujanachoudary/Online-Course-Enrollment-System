# main.py
from src.services.student_service import StudentService
from src.services.enrollment_service import EnrollmentService
from src.services.payment_service import PaymentService
from src.services.admin_service import AdminService

from src.dao.student_dao import StudentDAO
from src.dao.enrollment_dao import EnrollmentDAO
from src.dao.payment_dao import PaymentDAO
from src.dao.course_dao import CourseDAO

def main_menu():
    # Initialize DAOs
    student_dao = StudentDAO()
    enrollment_dao = EnrollmentDAO()
    payment_dao = PaymentDAO()
    course_dao = CourseDAO()

    # Pass DAOs into Services
    student_service = StudentService(student_dao)
    enrollment_service = EnrollmentService(enrollment_dao)
    payment_service = PaymentService(payment_dao, enrollment_dao)
    admin_service = AdminService(course_dao, enrollment_dao)


    while True:
        print("\n===== Online Course Enrollment System =====")
        print("1. Student Menu")
        print("2. Admin Menu")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            student_menu(student_service, enrollment_service, payment_service)
        elif choice == '2':
            admin_menu(admin_service)
        elif choice == '3':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

# ---------------------- Student Menu ---------------------- #
def student_menu(student_service, enrollment_service, payment_service):
    while True:
        print("\n--- Student Menu ---")
        print("1. Register")
        print("2. Login")
        print("3. View Details")
        print("4. Enroll in Course")
        print("5. Drop Course")
        print("6. View Enrollments")
        print("7. Make Payment")
        print("8. Logout")
        print("9. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            student_service.register_student()
        elif choice == '2':
            student_service.login_student()
        elif choice == '3':
            student_service.view_student_details()
        elif choice == '4':
            if student_service.current_student:
                student_id = student_service.current_student['student_id']
                course_id = input("Enter Course ID to enroll: ").strip()
                enrollment_service.enroll_course(student_id, course_id)
            else:
                print("Login first to enroll.")
        elif choice == '5':
            enrollment_id = input("Enter Enrollment ID to drop: ").strip()
            enrollment_service.drop_course(enrollment_id)
        elif choice == '6':
            if student_service.current_student:
                student_id = student_service.current_student['student_id']
                enrollment_service.view_student_enrollments(student_id)
            else:
                print("Login first to view enrollments.")
        elif choice == '7':
            enrollment_id = input("Enter Enrollment ID to pay for: ").strip()
            amount = float(input("Enter amount: ").strip())
            payment_service.pay_for_enrollment(enrollment_id, amount)
        elif choice == '8':
            student_service.logout_student()
        elif choice == '9':
            break
        else:
            print("Invalid choice. Try again.")

# ---------------------- Admin Menu ---------------------- #
def admin_menu(admin_service):
    while True:
        print("\n--- Admin Menu ---")
        print("1. Add Course")
        print("2. Edit Course")
        print("3. Delete Course")
        print("4. View Enrollments")
        print("5. Generate Reports")
        print("6. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            admin_service.add_course()
        elif choice == '2':
            admin_service.edit_course()
        elif choice == '3':
            admin_service.delete_course()
        elif choice == '4':
            admin_service.view_enrollments()
        elif choice == '5':
            admin_service.generate_reports()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Try again.")

# ---------------------- Entry Point ---------------------- #
if __name__ == "__main__":
    main_menu()
