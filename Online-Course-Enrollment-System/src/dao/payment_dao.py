# src/dao/payment_dao.py
from src.config import get_supabase

class PaymentDAO:
    def __init__(self):
        self.supabase = get_supabase()
        self.table = "payment"  # Must match your Supabase table

    def add_payment(self, enrollment_id, amount):
        try:
            response = self.supabase.table(self.table).insert({
                "enrollment_id": enrollment_id,
                "amount": amount
            }).execute()

            if response.error:
                print("Error adding payment:", response.data)
                return None

            return response.data[0]["payment_id"]

        except Exception as e:
            print("Exception adding payment:", e)
            return None

    def get_payment_by_enrollment(self, enrollment_id):
        try:
            response = self.supabase.table(self.table).select("*").eq("enrollment_id", enrollment_id).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print("Exception fetching payment:", e)
            return None

    def get_all_payments(self):
        """
        Returns all payments, used by Admin for reports
        """
        try:
            response = self.supabase.table(self.table).select("*").execute()
            return response.data
        except Exception as e:
            print("Exception fetching all payments:", e)
            return []
