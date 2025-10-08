# src/dao/course_dao.py
from src.config import get_supabase

class CourseDAO:
    def __init__(self):
        self.supabase = get_supabase()
        self.table = "courses"

    def add_course(self, title, credits, faculty):
        try:
            response = self.supabase.table(self.table).insert({
                "title": title,
                "credits": credits,
                "faculty": faculty
            }).execute()
            if response.error:
                print("Error adding course:", response.data)
                return None
            return response.data[0]["course_id"]
        except Exception as e:
            print("Exception adding course:", e)
            return None

    def edit_course(self, course_id, title=None, credits=None, faculty=None):
        update_data = {}
        if title:
            update_data["title"] = title
        if credits:
            update_data["credits"] = credits
        if faculty:
            update_data["faculty"] = faculty

        try:
            response = self.supabase.table(self.table).update(update_data).eq("course_id", course_id).execute()
            if response.error:
                print("Error updating course:", response.data)
                return False
            return True
        except Exception as e:
            print("Exception updating course:", e)
            return False

    def delete_course(self, course_id):
        try:
            response = self.supabase.table(self.table).delete().eq("course_id", course_id).execute()
            if response.error:
                print("Error deleting course:", response.data)
                return False
            return True
        except Exception as e:
            print("Exception deleting course:", e)
            return False

    def get_all_courses(self):
        try:
            response = self.supabase.table(self.table).select("*").execute()
            return response.data
        except Exception as e:
            print("Exception fetching courses:", e)
            return []
