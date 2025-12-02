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
    def get_by_id(course_id):
        """Get course by ID"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM course WHERE course_id = %s", (course_id,))
        course = cursor.fetchone()
        conn.close()
        return course

    @staticmethod
    def search(course_id=None, name=None, program_id=None):
        """Search courses by various criteria"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM course WHERE 1=1"
        values = []

        if course_id:
            query += " AND course_id = %s"
            values.append(course_id)
        if name:
            query += " AND course_name LIKE %s"
            values.append("%" + name + "%")
        if program_id:
            query += " AND program_id = %s"
            values.append(program_id)

        cursor.execute(query, tuple(values))
        courses = cursor.fetchall()
        conn.close()
        return courses

    @staticmethod
    def create(course_name, course_code, program_id, credits, description):
        """Create a new course"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO course (course_name, course_code, program_id, credits, description)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (course_name, course_code, program_id, credits, description)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def update(course_id, **kwargs):
        """Update course fields dynamically"""
        conn = get_connection()
        cursor = conn.cursor()

        fields = []
        values = []

        for key, value in kwargs.items():
            if value is not None:
                fields.append(f"{key} = %s")
                values.append(value)

        if fields:
            query = f"UPDATE course SET {', '.join(fields)} WHERE course_id = %s"
            values.append(course_id)
            cursor.execute(query, tuple(values))
            conn.commit()

        conn.close()

    @staticmethod
    def delete(course_id):
        """Delete a course"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM course WHERE course_id = %s", (course_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def code_exists(course_code):
        """Check if course code already exists"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM course WHERE course_code = %s", (course_code,))
        exists = cursor.fetchone()[0] > 0
        conn.close()
        return exists
