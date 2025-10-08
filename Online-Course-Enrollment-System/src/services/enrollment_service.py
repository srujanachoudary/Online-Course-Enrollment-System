# src/services/enrollment_service.py
class EnrollmentService:
    def __init__(self, enrollment_dao):
        self.enrollment_dao = enrollment_dao

    def enroll_course(self, student_id, course_id):
        enrollment_id = self.enrollment_dao.enroll_student(student_id, course_id)
        if enrollment_id:
            print(f"Enrollment successful. Enrollment ID: {enrollment_id}")
        else:
            print("Enrollment failed.")

    def drop_course(self, enrollment_id):
        success = self.enrollment_dao.drop_enrollment(enrollment_id)
        print("Enrollment dropped." if success else "Failed to drop enrollment.")

    def view_student_enrollments(self, student_id):
        enrollments = self.enrollment_dao.get_enrollments_by_student(student_id)
        if not enrollments:
            print("No enrollments found.")
            return
        print("\n--- Your Enrollments ---")
        for e in enrollments:
            # adapt keys to your table columns
            print(f"Enrollment ID: {e.get('enrollment_id')}, Course ID: {e.get('course_id')}, Status: {e.get('status', 'N/A')}")
