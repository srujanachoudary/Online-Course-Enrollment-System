# src/dao/student_dao.py
from src.config import get_supabase

class StudentDAO:
    def __init__(self):
        self.supabase = get_supabase()
        self.table = "students" 

    def add_student(self, name, email, department, phone):
        try:
            response = self.supabase.table(self.table).insert({
                "name": name,
                "email": email,
                "department": department,
                "phone": phone
            }).execute()

            if response.error:
                print("Error adding student:", response.data)
                return None
            return response.data[0]["student_id"]

        except Exception as e:
            print("Exception adding student:", e)
            return None

    def get_student_by_email(self, email):
        try:
            response = self.supabase.table(self.table).select("*").eq("email", email).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print("Exception fetching student by email:", e)
            return None
