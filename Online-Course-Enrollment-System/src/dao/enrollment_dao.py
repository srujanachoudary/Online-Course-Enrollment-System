# src/dao/enrollment_dao.py
from src.config import get_supabase

class EnrollmentDAO:
    def __init__(self):
        self.supabase = get_supabase()
        self.table = "enrollment"  # Must match your Supabase table

    def enroll_student(self, student_id, course_id):
        try:
            response = self.supabase.table(self.table).insert({
                "student_id": student_id,
                "course_id": course_id
            }).execute()

            if getattr(response, "error", None):
                print("Error enrolling student:", response.error)
                return None

            return response.data[0]["enrollment_id"]

        except Exception as e:
            print("Exception enrolling student:", e)
            return None

    def drop_enrollment(self, enrollment_id):
        try:
            response = self.supabase.table(self.table).delete().eq("enrollment_id", enrollment_id).execute()
            if getattr(response, "error", None):
                print("Error dropping enrollment:", response.error)
                return False
            return True
        except Exception as e:
            print("Exception dropping enrollment:", e)
            return False

    def get_enrollments_by_student(self, student_id):
        try:
            query = self.supabase.table(self.table).select("*")
            if student_id:  # If student_id is provided, filter by it
                query = query.eq("student_id", student_id)
            response = query.execute()
            return response.data
        except Exception as e:
            print("Exception fetching enrollments:", e)
            return []

    def get_all_enrollments(self):
        """
        Returns all enrollments, used by Admin for reports
        """
        return self.get_enrollments_by_student("")  # empty string = no filter

    def update_status(self, enrollment_id, status):
        """
        Update the status of an enrollment (e.g., Pending -> Paid)
        """
        try:
            response = self.supabase.table(self.table).update({
                "status": status
            }).eq("enrollment_id", enrollment_id).execute()

            if getattr(response, "error", None):
                print("Error updating enrollment status:", response.error)
                return False
            return True

        except Exception as e:
            print("Exception updating enrollment status:", e)
            return False
