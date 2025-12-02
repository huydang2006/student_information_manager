# app/routes/courses.py
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from app.services.course_service import CourseService
from app.models.course_model import Course

courses_bp = Blueprint('courses', __name__, url_prefix='/courses', template_folder='../templates')


@courses_bp.route('/')
def list():
    """Display list of courses"""
    courses = CourseService.get_all_courses()
    return render_template('courses/list.html', courses=courses)


@courses_bp.route('/view/<int:course_id>')
def view(course_id):
    """View course details"""
    course = CourseService.get_course_by_id(course_id)
    if not course:
        flash('Course not found', 'danger')
        return redirect(url_for('courses.list'))
    return render_template('courses/list.html', courses=[course])


@courses_bp.route('/search', methods=['GET', 'POST'])
def search():
    """Search courses"""
    if request.method == 'POST':
        course_id = request.form.get('course_id')
        name = request.form.get('name')
        program_id = request.form.get('program_id')

        courses = CourseService.search_courses(
            course_id=course_id,
            name=name,
            program_id=program_id
        )
        return render_template('courses/list.html', courses=courses)
    
    return redirect(url_for('courses.list'))


@courses_bp.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new course"""
    if request.method == 'GET':
        programs = Course.get_all()  # Get programs
        return render_template('courses/form.html', programs=programs)

    # Handle POST request
    data = {
        'course_name': request.form.get('course_name'),
        'course_code': request.form.get('course_code'),
        'program_id': request.form.get('program_id'),
        'credits': request.form.get('credits'),
        'description': request.form.get('description')
    }

    success, message = CourseService.create_course(data)
    if success:
        flash(message, 'success')
        return redirect(url_for('courses.list'))
    else:
        flash(message if isinstance(message, str) else ', '.join(message), 'danger')
        return redirect(url_for('courses.create'))


@courses_bp.route('/update/<int:course_id>', methods=['GET', 'POST'])
def update(course_id):
    """Update course"""
    course = CourseService.get_course_by_id(course_id)
    if not course:
        flash('Course not found', 'danger')
        return redirect(url_for('courses.list'))

    if request.method == 'GET':
        programs = Course.get_all()
        return render_template('courses/form.html', course=course, programs=programs)

    # Handle POST request
    data = {}
    if request.form.get('course_name'):
        data['course_name'] = request.form.get('course_name')
    if request.form.get('course_code'):
        data['course_code'] = request.form.get('course_code')
    if request.form.get('program_id'):
        data['program_id'] = request.form.get('program_id')
    if request.form.get('credits'):
        data['credits'] = request.form.get('credits')
    if request.form.get('description'):
        data['description'] = request.form.get('description')

    success, message = CourseService.update_course(course_id, data)
    if success:
        flash(message, 'success')
        return redirect(url_for('courses.list'))
    else:
        flash(message if isinstance(message, str) else ', '.join(message), 'danger')
        return redirect(url_for('courses.update', course_id=course_id))


@courses_bp.route('/delete/<int:course_id>', methods=['POST'])
def delete(course_id):
    """Delete course"""
    success, message = CourseService.delete_course(course_id)
    if success:
        return jsonify({'success': True, 'message': message})
    return jsonify({'success': False, 'message': message}), 400
