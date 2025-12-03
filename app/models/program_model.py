# app/models/course_model.py
from app.connection import get_connection


class Program:
    """Program model for database operations"""

    @staticmethod
    def get_all():
        """Get all programs"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM program")
        courses = cursor.fetchall()
        conn.close()
        return courses

    @staticmethod
    def get_by_id(program_id):
        """Get program by ID"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM program WHERE program_id = %s", (program_id,))
        course = cursor.fetchone()
        conn.close()
        return course

    @staticmethod
    def search(program_id=None, name=None):
        """Search programs by various criteria"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM program WHERE 1=1"
        values = []

        if program_id:
            query += " AND program_id = %s"
            values.append(program_id)
        if name:
            query += " AND program_name LIKE %s"
            values.append("%" + name + "%")

        cursor.execute(query, tuple(values))
        programs = cursor.fetchall()
        conn.close()
        return programs

    # @staticmethod
    # def create(course_name, course_code, program_id, credits, description):
    #     """Create a new course"""
    #     conn = get_connection()
    #     cursor = conn.cursor()
        
    #     cursor.execute(
    #         """
    #         INSERT INTO course (course_name, course_code, program_id, credits, description)
    #         VALUES (%s, %s, %s, %s, %s)
    #         """,
    #         (course_name, course_code, program_id, credits, description)
    #     )
    #     conn.commit()
    #     conn.close()

    # @staticmethod
    # def update(course_id, **kwargs):
    #     """Update course fields dynamically"""
    #     conn = get_connection()
    #     cursor = conn.cursor()

    #     fields = []
    #     values = []

    #     for key, value in kwargs.items():
    #         if value is not None:
    #             fields.append(f"{key} = %s")
    #             values.append(value)

    #     if fields:
    #         query = f"UPDATE course SET {', '.join(fields)} WHERE course_id = %s"
    #         values.append(course_id)
    #         cursor.execute(query, tuple(values))
    #         conn.commit()

    #     conn.close()

    @staticmethod
    def delete(program_id):
        """Delete a program"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM program WHERE program_id = %s", (program_id,))
        conn.commit()
        conn.close()

    # @staticmethod
    # def code_exists(course_code):
    #     """Check if course code already exists"""
    #     conn = get_connection()
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT COUNT(*) FROM course WHERE course_code = %s", (course_code,))
    #     exists = cursor.fetchone()[0] > 0
    #     conn.close()
    #     return exists
