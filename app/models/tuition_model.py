# app/models/tuition_model.py
from app.connection import get_connection

class Tuition:
    """Student model for database operations"""

    @staticmethod
    def get_all():
        """Get all students with program information"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT
                s.*,
                p.full_name
            FROM tuition_fee s
            LEFT JOIN student p ON s.student_id = p.student_id
        """
        cursor.execute(query)
        students = cursor.fetchall()
        conn.close()
        return students

    @staticmethod
    def get_payments(fee_id):
        """Get payment by ID"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT *
            FROM payment
            WHERE fee_id = %s
            """
        
        cursor.execute(query,(fee_id,))
        payments = cursor.fetchall()
        conn.close()
        return payments

    @staticmethod
    def search(fee_id, name, semester, status):
        """Search tuition"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT s.*, p.full_name
            FROM tuition_fee s
            LEFT JOIN student p ON s.student_id = p.student_id
            WHERE 1=1
        """
        values = []

        if fee_id:
            query += " AND s.fee_id = %s"
            values.append(fee_id)
        if name:
            query += " AND p.full_name LIKE %s"
            values.append("%" + name + "%")
        if semester:
            query += " AND s.semester = %s"
            values.append(semester)
        if status:
            query += " AND s.payment_status = %s"
            values.append(status)

        cursor.execute(query, tuple(values))
        tuitions = cursor.fetchall()
        conn.close()
        return tuitions 
    
    @staticmethod
    def delete(fee_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            # Thực thi lệnh xóa
            cursor.execute("DELETE FROM tuition_fee WHERE fee_id = %s", (fee_id,))
            conn.commit()
            
            rows_deleted = cursor.rowcount
            cursor.close()
            conn.close()

            if rows_deleted > 0:
                return True
            else:
                return False
        except Exception as e:
            # Nếu lỗi khóa ngoại (do đã có payment), in ra và trả về False
            print(f"DB Error: {e}")
            if conn:
                conn.rollback()
                conn.close()
            return False    

    @staticmethod
    def update(fee_id, **kwargs):
        """Update Tuition fields dynamically"""
        conn = get_connection()
        cursor = conn.cursor()

        fields = []
        values = []

        for key, value in kwargs.items():
            if value is not None:
                fields.append(f"{key} = %s")
                values.append(value)

        if fields:
            query = f"UPDATE tuition_fee SET {', '.join(fields)} WHERE fee_id = %s"
            values.append(fee_id)
            cursor.execute(query, tuple(values))
            conn.commit()

        conn.close()

    @staticmethod
    def add_payment(fee_id, amount, payment_method, code, collected_by, remarks):
        """ add payment"""
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO payment (fee_id, amount, payment_method, transaction_code, collected_by, remarks)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (fee_id, amount, payment_method, code, collected_by, remarks))

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def add_tuition(student_id, semester, academic_year, total_amount):
        """ add payment"""
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO tuition_fee (student_id, academic_year, semester, total_amount)
                VALUES (%s, %s, %s, %s)
            """, (student_id, academic_year, semester, total_amount))

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_year():
        """ Get academic year exits"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT DISTINCT academic_year FROM tuition_fee ORDER BY academic_year DESC"
        
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return data