# app/routes/students.py
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, Response
from app.services.student_service import StudentService
from app.models.student_model import Student
from app.models.program_model import Program
from app.models.course_model import Course
import csv
from io import StringIO

students_bp = Blueprint('students', __name__, url_prefix='/students', template_folder='../templates')


@students_bp.route('/')
def list():
    """Display list of students"""
    students = StudentService.get_all_students()
    return render_template('students/list.html', students=students)


@students_bp.route('/view/<int:student_id>')
def view(student_id):
    """View student details"""
    student = StudentService.get_student_by_id(student_id)
    enrollments = StudentService.get_enrollments_student(student_id)
    courses = Course.get_all()
    if not student:
        flash('Student not found', 'danger')
        return redirect(url_for('students.list'))
    return render_template('students/detail.html', student=student, enrollments=enrollments, courses=courses)


@students_bp.route('/search', methods=['GET', 'POST'])
def search():
    """Search students"""
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        name = request.form.get('name')
        program_id = request.form.get('program_id')
        enrollment_year = request.form.get('enrollment_year')

        students = StudentService.search_students(
            student_id=student_id,
            name=name,
            program_id=program_id,
            enrollment_year=enrollment_year
        )
        return render_template('students/list.html', students=students)
    
    return redirect(url_for('students.list'))


@students_bp.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new student"""
    if request.method == 'GET':
        programs = Program.get_all()  # Get programs
        return render_template('students/form.html', programs=programs)

    # Handle POST request
    data = {
        'full_name': request.form.get('full_name'),
        'email': request.form.get('email'),
        'phone_number': request.form.get('phone_number'),
        'address': request.form.get('address'),
        'date_of_birth': request.form.get('date_of_birth'),
        'gender': request.form.get('gender'),
        'program_id': request.form.get('program_id'),
        'enrollment_year': request.form.get('enrollment_year')
    }

    success, message = StudentService.create_student(data)
    if success:
        flash(message, 'success')
        return redirect(url_for('students.list'))
    else:
        flash(message if isinstance(message, str) else ', '.join(message), 'danger')
        return redirect(url_for('students.create'))


@students_bp.route('/update/<int:student_id>', methods=['GET', 'POST'])
def update(student_id):
    """Update student"""
    student = StudentService.get_student_by_id(student_id)
    if not student:
        flash('Student not found', 'danger')
        return redirect(url_for('students.list'))

    if request.method == 'GET':
        programs = Program.get_all()
        return render_template('students/form.html', student=student, programs=programs)

    # Handle POST request
    data = {}
    if request.form.get('full_name'):
        data['full_name'] = request.form.get('full_name')
    if request.form.get('email'):
        data['email'] = request.form.get('email')
    if request.form.get('phone_number'):
        data['phone_number'] = request.form.get('phone_number')
    if request.form.get('address'):
        data['address'] = request.form.get('address')
    if request.form.get('date_of_birth'):
        data['date_of_birth'] = request.form.get('date_of_birth')
    if request.form.get('gender'):
        data['gender'] = request.form.get('gender')
    if request.form.get('program_id'):
        data['program_id'] = request.form.get('program_id')
    if request.form.get('enrollment_year'):
        data['enrollment_year'] = request.form.get('enrollment_year')

    success, message = StudentService.update_student(student_id, data)
    if success:
        flash(message, 'success')
        return redirect(url_for('students.view', student_id=student_id))
    else:
        flash(message if isinstance(message, str) else ', '.join(message), 'danger')
        return redirect(url_for('students.update', student_id=student_id))


@students_bp.route('/delete/<int:student_id>', methods=['POST'])
def delete(student_id):
    """Delete student"""
    success, message = StudentService.delete_student(student_id)
    if success:
        return jsonify({'success': True, 'message': message})
    return jsonify({'success': False, 'message': message}), 400

@students_bp.route('/deleteEnrollment/<int:enrollment_id>', methods=['POST'])
def deleteEnrollment(enrollment_id):
    """Delete enrollment"""
    success, message = StudentService.delete_enrollment(enrollment_id)
    if success:
        return jsonify({'success': True, 'message': message})
    return jsonify({'success': False, 'message': message}), 400

@students_bp.route('/addenrollment/<int:student_id>', methods=['GET', 'POST'])
def add_enrollment(student_id):
    """Create a new enrollment"""

    # Handle POST request
    data = {
        'student_id': student_id,
        'course_id': request.form.get('course_id'),
        'semester': request.form.get('semester'),
        'academic_year': request.form.get('academic_year')
    }

    success, message = StudentService.create_enrollment(data)
    if success:
        flash(message, 'success')
        return redirect(url_for('students.view', student_id=student_id))
    else:
        flash(message if isinstance(message, str) else ', '.join(message), 'danger')
        return redirect(url_for('students.view', student_id=student_id))
    

@students_bp.route('/updateEnrollment/<int:student_id>', methods=['GET', 'POST'])
def updateEnrollment(student_id):
    # Handle POST request

    enrollment_id = request.form.get('enrollment_id')
    academic_year = request.form.get('academic_year')
    grade = request.form.get('grade')
    status = request.form.get('status')

    success, message = StudentService.update_enrollment(enrollment_id, academic_year, grade, status)
    if success:
        flash(message, 'success')
        return redirect(url_for('students.view', student_id=student_id))
    else:
        flash(message if isinstance(message, str) else ', '.join(message), 'danger')
        return redirect(url_for('students.view', student_id=student_id))
    
@students_bp.route("/export/grade-distribution")
def export_grade_distribution():
    # Lấy dữ liệu từ SQL
    data = Student.get_all()
    # data là danh sách dict: [{"grade_range": "0-1", "total_students": 20}, ...]

    # Tạo buffer CSV trong RAM
    si = StringIO()
    writer = csv.writer(si)

    # Ghi header
    writer.writerow(["student_id","full_name","date_of_birth","gender","email","phone_number","address","program_id","enrollment_year"])

    # Ghi từng dòng
    for row in data:
        writer.writerow([row["student_id"], row["full_name"], row["date_of_birth"], row["gender"], row["email"], row["phone_number"], row["address"], row["program_id"], row["enrollment_year"]])

    # Tạo response để tải xuống
    output = si.getvalue()
    response = Response(
        output,
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=student_information.csv"
        }
    )
    return response