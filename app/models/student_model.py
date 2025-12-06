# app/models/student_model.py
from app.connection import get_connection


class Student:
    """Student model for database operations"""

    @staticmethod
    def get_all():
        """Get all students with program information"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT
                s.*,
                p.program_name
            FROM student s
            LEFT JOIN program p ON s.program_id = p.program_id
        """
        cursor.execute(query)
        students = cursor.fetchall()
        conn.close()
        return students

    @staticmethod
    def get_by_id(student_id):
        """Get student by ID"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT 
                s.*,
                p.program_name,
                i.full_name AS advisor_name
            FROM student s
            LEFT JOIN program p 
                ON s.program_id = p.program_id
            LEFT JOIN advisor_assignment aa 
                ON s.student_id = aa.student_id
            LEFT JOIN instructor i 
                ON aa.instructor_id = i.instructor_id
            WHERE s.student_id = %s
            """,
            (student_id,)
        )
        student = cursor.fetchone()
        conn.close()
        return student

    @staticmethod
    def search(student_id=None, name=None, program_id=None, enrollment_year=None):
        """Search students by various criteria"""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT s.*, p.program_name
            FROM student s
            LEFT JOIN program p ON s.program_id = p.program_id
            WHERE 1=1
        """
        values = []

        if student_id:
            query += " AND s.student_id = %s"
            values.append(student_id)
        if name:
            query += " AND s.full_name LIKE %s"
            values.append("%" + name + "%")
        if program_id:
            query += " AND s.program_id = %s"
            values.append(program_id)
        if enrollment_year:
            query += " AND s.enrollment_year = %s"
            values.append(enrollment_year)

        cursor.execute(query, tuple(values))
        students = cursor.fetchall()
        conn.close()
        return students

    @staticmethod
    def create(full_name, email, phone_number, address, date_of_birth, gender, program_id, enrollment_year):
        """Create a new student"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO student
            (full_name, email, phone_number, address, date_of_birth, gender, program_id, enrollment_year)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (full_name, email, phone_number, address, date_of_birth, gender, program_id, enrollment_year)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def update(student_id, **kwargs):
        """Update student fields dynamically"""
        conn = get_connection()
        cursor = conn.cursor()

        fields = []
        values = []

        for key, value in kwargs.items():
            if value is not None:
                fields.append(f"{key} = %s")
                values.append(value)

        if fields:
            query = f"UPDATE student SET {', '.join(fields)} WHERE student_id = %s"
            values.append(student_id)
            cursor.execute(query, tuple(values))
            conn.commit()

        conn.close()

    @staticmethod
    def delete(student_id):
        """Delete a student"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM student WHERE student_id = %s", (student_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def email_exists(email):
        """Check if email already exists"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM student WHERE email = %s", (email,))
        exists = cursor.fetchone()[0] > 0
        conn.close()
        return exists
    
    @staticmethod
    def get_enrollments(student_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT
                e.enrollment_id,
                s.full_name AS student_name,
                c.course_name,
                e.semester,
                e.academic_year,
                e.grade,
                e.status
            FROM enrollment e
            INNER JOIN student s ON e.student_id = s.student_id
            INNER JOIN course c ON e.course_id = c.course_id
            WHERE e.student_id = %s
            ORDER BY e.academic_year DESC, e.semester;
        """

        cursor.execute(query, (student_id,))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result
    
    @staticmethod
    def deleteEnrollment(enrollment_id):
        """Delete a student"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM enrollment WHERE enrollment_id = %s", (enrollment_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def createEnrollment(student_id, course_id, semester, academic_year, grade = None, status = 'Enrolled'):
        """Create a new enrollment"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO enrollment
            (student_id, course_id, semester, academic_year, grade, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (student_id, course_id, semester, academic_year, grade, status)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def updateenrollment(enrollment_id, academic_year, grade, status):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            UPDATE enrollment
            SET academic_year = %s,
                grade = %s,
                status = %s
            WHERE enrollment_id = %s
        """
        cursor.execute(query, (academic_year, grade, status, enrollment_id,))
        conn.commit()
        conn.close()