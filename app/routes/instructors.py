# app/routes/instructors.py
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from app.services.instructor_service import InstructorService

instructors_bp = Blueprint('instructors', __name__, url_prefix='/instructors', template_folder='../templates')


@instructors_bp.route('/')
def list():
    """Display list of instructors"""
    instructors = InstructorService.get_all_instructors()
    return render_template('instructors/list.html', instructors=instructors)


@instructors_bp.route('/view/<int:instructor_id>')
def view(instructor_id):
    """View instructor details"""
    instructor = InstructorService.get_instructor_by_id(instructor_id)
    if not instructor:
        flash('Instructor not found', 'danger')
        return redirect(url_for('instructors.list'))
    return render_template('instructors/list.html', instructors=[instructor])


@instructors_bp.route('/search', methods=['GET', 'POST'])
def search():
    """Search instructors"""
    if request.method == 'POST':
        instructor_id = request.form.get('instructor_id')
        name = request.form.get('name')
        email = request.form.get('email')

        instructors = InstructorService.search_instructors(
            instructor_id=instructor_id,
            name=name,
            email=email
        )
        return render_template('instructors/list.html', instructors=instructors)
    
    return redirect(url_for('instructors.list'))


@instructors_bp.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new instructor"""
    if request.method == 'GET':
        return render_template('instructors/form.html')

    # Handle POST request
    data = {
        'full_name': request.form.get('full_name'),
        'email': request.form.get('email'),
        'specialization': request.form.get('specialization'),
        'office_location': request.form.get('office_location')
    }

    success, message = InstructorService.create_instructor(data)
    if success:
        flash(message, 'success')
        return redirect(url_for('instructors.list'))
    else:
        flash(message if isinstance(message, str) else ', '.join(message), 'danger')
        return redirect(url_for('instructors.create'))


@instructors_bp.route('/update/<int:instructor_id>', methods=['GET', 'POST'])
def update(instructor_id):
    """Update instructor"""
    instructor = InstructorService.get_instructor_by_id(instructor_id)
    if not instructor:
        flash('Instructor not found', 'danger')
        return redirect(url_for('instructors.list'))

    if request.method == 'GET':
        return render_template('instructors/form.html', instructor=instructor)

    # Handle POST request
    data = {}
    if request.form.get('full_name'):
        data['full_name'] = request.form.get('full_name')
    if request.form.get('email'):
        data['email'] = request.form.get('email')
    if request.form.get('specialization'):
        data['specialization'] = request.form.get('specialization')
    if request.form.get('office_location'):
        data['office_location'] = request.form.get('office_location')

    success, message = InstructorService.update_instructor(instructor_id, data)
    if success:
        flash(message, 'success')
        return redirect(url_for('instructors.list'))
    else:
        flash(message if isinstance(message, str) else ', '.join(message), 'danger')
        return redirect(url_for('instructors.update', instructor_id=instructor_id))


@instructors_bp.route('/delete/<int:instructor_id>', methods=['POST'])
def delete(instructor_id):
    """Delete instructor"""
    success, message = InstructorService.delete_instructor(instructor_id)
    if success:
        return jsonify({'success': True, 'message': message})
    return jsonify({'success': False, 'message': message}), 400
