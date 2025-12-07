# app/routes/students.py
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from app.models.student_model import Student
from app.models.instructor_model import Instructor
from app.models.program_model import Program
from app.models.course_model import Course
from app.services.home_service import DashboardService
from app.models.home import Dashboard
import plotly.express as px
import plotly.io as pio

home_bp = Blueprint('home', __name__, url_prefix='/home', template_folder='../templates')

@home_bp.route("/")
def describe():
    # Tuition Chart
    tuition_chart = DashboardService.tuition_summary()

    # Top of GPA
    top_gpa = Dashboard.get_top_gpa()

    # Grade Distribution
    grade_distribution = DashboardService.grade_distribution()

    # Number of student
    students = Student.get_all()
    number_of_student = len(students)

    # number of instructor
    instructors = Instructor.get_all()
    number_of_instructor = len(instructors)

    # number of program
    programs = Program.get_all()
    number_of_program = len(programs)

    # number of course
    course = Course.get_all()
    number_of_course = len(course)

    # Get Year exits in tuition
    years = DashboardService.year()

    return render_template("home.html", tuition_chart=tuition_chart, 
                                        grade_distribution=grade_distribution, 
                                        top_gpa=top_gpa,
                                        number_of_student=number_of_student,
                                        number_of_instructor=number_of_instructor,
                                        number_of_program=number_of_program,
                                        number_of_course=number_of_course,
                                        years=years
                                        )

@home_bp.route("/api/tuition_filter")
def api_tuition_filter():
    year = request.args.get("year")
    sem = request.args.get("semester")

    if year == "":
        year = None
    if sem == "":
        sem = None

    total = DashboardService.calculate_tuition(year, sem)  # bạn tự định nghĩa hàm này

    return jsonify({
        "total": total
    })