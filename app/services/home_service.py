from app.models.student_model import Student
from app.models.tuition_model import Tuition
from app.models.home import Dashboard
import plotly.express as px
import plotly.io as pio

class DashboardService:
    @staticmethod
    def number_of_student():
        student = Student.get_all()
        number_of_student = len(student)
        return number_of_student
    
    @staticmethod
    def number_of_program():
        None
    
    @staticmethod
    def number_of_course():
        None

    @staticmethod
    def nummber_of_instructor():
        None
    
    @staticmethod
    def tuition_summary():
        summary = Dashboard.get_tuition_summary()

        labels = [f"{row['payment_status']} ({row['total_count']})" for row in summary]
        values = [row["total_count"] for row in summary]

        fig = px.pie(values=values, names=labels)

        # Màu sắc tuỳ chỉnh
        fig.update_traces(
            marker=dict(colors=['#5dade2', '#ec7063', '#52be80']),
            textinfo='percent',   # hiển thị phần trăm
            textfont=dict(size=20)
        )

        fig.update_layout(
            paper_bgcolor='rgb(30,35,44)',
            plot_bgcolor='rgb(30,35,44)',
            font=dict(color='white', size=16),
            legend=dict(
                font=dict(size=25),  # tăng kích thước legend
                bgcolor='rgba(0,0,0,0)'  # nền trong suốt
            )
        )

        chart_html = pio.to_html(fig, full_html=False)
        return chart_html


    @staticmethod
    def grade_distribution():
        data = Dashboard.get_grade_distribution()

        fig = px.bar(
            data,
            x="grade_range",
            y="total_students",
            labels={"grade_range": "Grade range", "total_students": "Total students"},
            text="total_students"
        )

        fig.update_traces(textposition='outside')
        fig.update_layout(
            paper_bgcolor='rgb(30,35,44)',
            plot_bgcolor='rgb(30,35,44)',
            font=dict(color='white'),
        )
        fig.update_traces(marker_color='rgba(80,150,255,0.8)')

        # Tạo HTML div của Plotly (không full page)
        chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

        # Truyền vào template
        return chart_html
    
    @staticmethod
    def calculate_tuition(year, sem):
        data = Dashboard.get_tuition(year = year, semester = sem)

        if not data:
            return 0
        
        # Sum tổng học phí
        total_amount = sum(item["total_amount"] for item in data)

        return total_amount

    @staticmethod
    def year():
        years = Tuition.get_year()
        year = [item['academic_year'] for item in years]
        return year
    
        