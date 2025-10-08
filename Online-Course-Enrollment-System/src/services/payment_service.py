# src/services/payment_service.py
class PaymentService:
    def __init__(self, payment_dao, enrollment_dao):
        self.payment_dao = payment_dao
        self.enrollment_dao = enrollment_dao

    def pay_for_enrollment(self, enrollment_id, amount):
        payment_id = self.payment_dao.add_payment(enrollment_id, amount)
        if payment_id:
            updated = self.enrollment_dao.update_status(enrollment_id, "Paid")
            if updated:
                print(f"Payment successful. Payment ID: {payment_id}. Enrollment marked as Paid.")
            else:
                print(f"Payment succeeded (ID {payment_id}) but failed to update enrollment status.")
        else:
            print("Payment failed.")
