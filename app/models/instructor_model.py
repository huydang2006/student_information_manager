# app/models/instructor_model.py
from app.connection import get_connection


class Instructor:
    """Instructor model for database operations"""

    @staticmethod
    def get_all():
        """Get all instructors"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM instructor")
        instructors = cursor.fetchall()
        conn.close()
        return instructors

    @staticmethod
    def get_by_id(instructor_id):
        """Get instructor by ID"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM instructor WHERE instructor_id = %s", (instructor_id,))
        instructor = cursor.fetchone()
        conn.close()
        return instructor

    @staticmethod
    def search(instructor_id=None, name=None, email=None):
        """Search instructors by various criteria"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM instructor WHERE 1=1"
        values = []

        if instructor_id:
            query += " AND instructor_id = %s"
            values.append(instructor_id)
        if name:
            query += " AND full_name LIKE %s"
            values.append("%" + name + "%")
        if email:
            query += " AND email = %s"
            values.append(email)

        cursor.execute(query, tuple(values))
        instructors = cursor.fetchall()
        conn.close()
        return instructors

    @staticmethod
    def create(full_name, email, specialization, office_location):
        """Create a new instructor"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO instructor (full_name, email, specialization, office_location)
            VALUES (%s, %s, %s, %s)
            """,
            (full_name, email, specialization, office_location)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def update(instructor_id, **kwargs):
        """Update instructor fields dynamically"""
        conn = get_connection()
        cursor = conn.cursor()

        fields = []
        values = []

        for key, value in kwargs.items():
            if value is not None:
                fields.append(f"{key} = %s")
                values.append(value)

        if fields:
            query = f"UPDATE instructor SET {', '.join(fields)} WHERE instructor_id = %s"
            values.append(instructor_id)
            cursor.execute(query, tuple(values))
            conn.commit()

        conn.close()

    @staticmethod
    def delete(instructor_id):
        """Delete an instructor"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM instructor WHERE instructor_id = %s", (instructor_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def email_exists(email):
        """Check if email already exists"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM instructor WHERE email = %s", (email,))
        exists = cursor.fetchone()[0] > 0
        conn.close()
        return exists
