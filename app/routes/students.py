# app/routes/students.py
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from app.services.student_service import StudentService
from app.models.course_model import Course

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
    if not student:
        flash('Student not found', 'danger')
        return redirect(url_for('students.list'))
    return render_template('students/detail.html', student=student)


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
        programs = Course.get_all()  # Get programs
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
        programs = Course.get_all()
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
