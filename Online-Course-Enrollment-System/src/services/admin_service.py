# src/services/admin_service.py
class AdminService:
    def __init__(self, course_dao, enrollment_dao, payment_dao=None):
        self.course_dao = course_dao
        self.enrollment_dao = enrollment_dao
        self.payment_dao = payment_dao

    def add_course(self):
        print("\n--- Add Course ---")
        title = input("Enter course title: ").strip()
        credits_input = input("Enter credits: ").strip()
        try:
            credits = int(credits_input)
        except:
            print("Invalid credits value.")
            return
        faculty = input("Enter faculty name: ").strip()
        course_id = self.course_dao.add_course(title, credits, faculty)
        print(f"Course added with ID {course_id}" if course_id else "Failed to add course.")

    def edit_course(self):
        print("\n--- Edit Course ---")
        course_id = input("Enter Course ID to edit: ").strip()
        title = input("New title (leave blank to skip): ").strip() or None
        credits_input = input("New credits (leave blank to skip): ").strip()
        credits = int(credits_input) if credits_input else None
        faculty = input("New faculty (leave blank to skip): ").strip() or None
        success = self.course_dao.edit_course(course_id, title, credits, faculty)
        print("Course updated." if success else "Failed to update course.")

    def delete_course(self):
        print("\n--- Delete Course ---")
        course_id = input("Enter Course ID to delete: ").strip()
        success = self.course_dao.delete_course(course_id)
        print("Course deleted." if success else "Failed to delete course.")

    def view_enrollments(self):
        enrollments = self.enrollment_dao.get_all_enrollments()
        if not enrollments:
            print("No enrollments.")
            return
        print("\n--- All Enrollments ---")
        for e in enrollments:
            print(f"Enrollment ID: {e.get('enrollment_id')}, Student: {e.get('student_id')}, Course: {e.get('course_id')}, Status: {e.get('status','N/A')}")

    def generate_reports(self):
        print("\n--- Reports ---")
        courses = self.course_dao.get_all_courses()
        enrollments = self.enrollment_dao.get_all_enrollments()
        for c in courses:
            cid = c.get('course_id')
            count = sum(1 for e in enrollments if e.get('course_id') == cid)
            print(f"{c.get('title')} (ID {cid}) -> {count} students")
        if self.payment_dao:
            payments = self.payment_dao.get_all_payments()
            total = sum(float(p.get('amount', 0)) for p in payments)
            print(f"\nTotal payments: {len(payments)}, Amount sum: {total}")
