from app.connection import get_connection

class Dashboard:
    @staticmethod
    def get_tuition_summary():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM v_tuition_fee_summary")
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_top_gpa():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM v_top_gpa")
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_grade_distribution():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM v_grade_distribution")
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def get_tuition(year, semester):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT total_amount
            FROM tuition_fee
            WHERE 1=1
        """
        values = []

        if year:
            query += " AND academic_year = %s"
            values.append(year)
            
        if semester:
            query += " AND semester = %s"
            values.append(semester)

        cursor.execute(query, tuple(values))
        data = cursor.fetchall()
        conn.close()
        return data