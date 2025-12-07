# app/services/tuition_service.py
from app.models.tuition_model import Tuition
from app.models.student_model import Student
# from app.utils.validators import validate_student_data, validate_email


class TuitionService:
    """Business logic for tuition operations"""
    @staticmethod
    def get_all_tuition():
        tuitions = Tuition.get_all()
        return tuitions
    
    @staticmethod
    def get_payments_student(fee_id):
        return Tuition.get_payments(fee_id)
    
    @staticmethod
    def search_tuitions(fee_id=None,name=None,semester=None,status=None):
        return Tuition.search(fee_id, name, semester, status)
    
    @staticmethod
    def delete_tuition(fee_id):
        # Gọi xuống Model
        is_deleted = Tuition.delete(fee_id)
        
        if is_deleted:
            return True, "Xóa học phí thành công!"
        else:
            # Thông báo lỗi rõ ràng
            return False, "Không thể xóa học phí này. Có thể do ID không tồn tại hoặc dữ liệu này đang dính dáng đến các khoản Thanh toán (Payment) đã có."
        
    @staticmethod
    def update(fee_id, data):
        """Update Tuition"""
        #Update Status


        # Clean and convert optional fields
        data['total_amount'] = float(data['total_amount'].replace(',', '.')) if data.get('total_amount') else None
        data['amount_paid'] = float(data['amount_paid'].replace(',', '.')) if data.get('amount_paid') else None
        
        if data['amount_paid'] == 0:
            data['payment_status'] = "Unpaid"
        elif data['total_amount'] <= data['amount_paid']:
            data['payment_status'] = "Fully Paid"
        else:
            data['payment_status'] = "Partially Paid"


        # Update student
        Tuition.update(fee_id = fee_id, **data)
        return True, "Tuition updated successfully"

    @staticmethod
    def add_payment(fee_id, amount, method, code = None, collected_by=None, remarks=None):

        amount = float(amount.replace(',', '.'))
        try:
            Tuition.add_payment(fee_id, amount, method, code, collected_by, remarks)
            return True, "Payment added successfully"

        except Exception as e:
            # Lấy đúng message từ trigger MySQL
            return False, str(e)

    @staticmethod
    def add_tuition(student_id, semester, academic_year, total_amount):

        if int(total_amount) <= 0:
            return False, "Invalid Value"
        
        # students = Student.get_all()
        # if student_id not in students[student_id]:
        #     return False, "Student does not exits"
        
        total_amount = float(total_amount.replace(',', '.'))


        try:
            Tuition.add_tuition(student_id, semester, academic_year, total_amount)
            return True, "Payment added successfully"

        except Exception as e:
            # Lấy đúng message từ trigger MySQL
            return False, str(e)
