# app/models/program_model.py
from app.connection import get_connection


class Program:
    """Program model for database operations"""

    @staticmethod
    def get_all():
        """Get all programs"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM program")
        programs = cursor.fetchall()
        conn.close()
        return programs

    @staticmethod
    def get_by_id(program_id):
        """Get program by ID"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM program WHERE program_id = %s", (program_id,))
        program = cursor.fetchone()
        conn.close()
        return program

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
    
    @staticmethod
    def create(program_name, department, duration_year, degree_type):
        """Create a new student"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO program
            (program_name, department, duration_years, degree_type)
            VALUES (%s, %s, %s, %s)
            """,
            (program_name, department, duration_year, degree_type,)
        )
        conn.commit()
        conn.close()


    @staticmethod
    def delete(program_id):
        """Delete a program"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM program WHERE program_id = %s", (program_id,))
        conn.commit()
        conn.close()


    @staticmethod
    def update(program_id, **kwargs):
        """Update Program fields dynamically"""
        conn = get_connection()
        cursor = conn.cursor()

        fields = []
        values = []

        for key, value in kwargs.items():
            if value is not None:
                fields.append(f"{key} = %s")
                values.append(value)

        if fields:
            query = f"UPDATE program SET {', '.join(fields)} WHERE program_id = %s"
            values.append(program_id)
            cursor.execute(query, tuple(values))
            conn.commit()

        conn.close()

    @staticmethod
    def name_exists(program_name):
        """
        Check if program name already exists.
        exclude_id: dùng khi update (để không tính chính nó)
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT COUNT(*) AS cnt 
            FROM program 
            WHERE program_name = %s
        """
        cursor.execute(query, (program_name,))

        result = cursor.fetchone()
        conn.close()

        return result['cnt'] > 0

    @staticmethod
    def add_course(course_name, credit_hours, semester, program_id, instructor_id):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO course
                    (course_name, credit_hours, semester_offered, program_id, instructor_id)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (course_name, credit_hours, semester, program_id, instructor_id)
            )
            conn.commit()
            return True, "Course added successfully"
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            conn.close()

    def updatecourse(course_id, **kwargs):
        """Update Program fields dynamically"""
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
