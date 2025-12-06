# app/models/course_model.py
from app.connection import get_connection

class Course:
    """Course model for database operations"""

    @staticmethod
    def get_all():
        """Get all courses"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM course")
        courses = cursor.fetchall()
        conn.close()
        return courses
    
    @staticmethod
    def get_by_program_id(program_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.callproc("sp_courses_by_program", [program_id])

        # Đọc kết quả SELECT từ procedure
        for result in cursor.stored_results():
            data = result.fetchall()

        cursor.close()
        conn.close()
        return data
    
    @staticmethod
    def delete(course_id):
        """Delete Course"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM course WHERE course_id = %s", (course_id,))
        conn.commit()
        conn.close()
