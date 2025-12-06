# app/routes/students.py
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from app.services.tuition_service import TuitionService
from app.models.tuition_model import Tuition

tuitions_bp = Blueprint('tuitions', __name__, url_prefix='/financial', template_folder='../templates')

@tuitions_bp.route('/')
def list():
    """Display list of Tuition"""
    tuitions = TuitionService.get_all_tuition()
    return render_template('tuitions/list.html', tuitions=tuitions)

@tuitions_bp.route('/view/<int:fee_id>')
def view(fee_id):
    """View fee details"""
    payments = TuitionService.get_payments_student(fee_id)
    return render_template('tuitions/detail.html',fee_id = fee_id, payments=payments)

@tuitions_bp.route('/search', methods=['GET', 'POST'])
def search():
    """Search tuition"""
    if request.method == 'POST':
        fee_id = request.form.get('fee_id')
        name = request.form.get('name')
        semester = request.form.get('semester')
        status = request.form.get('status')

        if semester == "":
            semester = None
        if status == "":
            status = None

        tuitions = TuitionService.search_tuitions(
            fee_id=fee_id,
            name=name,
            semester=semester,
            status=status
        )
        return render_template('tuitions/list.html', tuitions=tuitions)
    
    return redirect(url_for('tuitions.list'))

@tuitions_bp.route('/delete/<int:fee_id>', methods=['POST'])
def delete(fee_id):
    """Delete tuition"""
    success, message = TuitionService.delete_tuition(fee_id)
    if success:
        return jsonify({'success': True, 'message': message})
    return jsonify({'success': False, 'message': message}), 400

@tuitions_bp.route("/payments/<int:fee_id>")
def get_payment(fee_id):
    payment = Tuition.get_payments(fee_id)
    return jsonify(payment)

@tuitions_bp.route('/update', methods=["GET","POST"])
def update():
    data = {}
    if request.form.get('fee_id'):
        fee_id = request.form.get('fee_id')
    if request.form.get('semester'):
        data['semester'] = request.form.get('semester')
    if request.form.get('total'):
        data['total_amount'] = request.form.get('total')
    if request.form.get('paid'):
        data['amount_paid'] = request.form.get('paid')

    success, message = TuitionService.update(fee_id, data)
    if success:
        flash(message, 'success')
        return redirect(url_for('tuitions.list'))
    else:
        flash(message if isinstance(message, str) else ', '.join(message), 'danger')
        return redirect(url_for('tuitions.list'))
    
@tuitions_bp.route('/add_payment/<int:fee_id>', methods=["GET","POST"])
def add_payment(fee_id):
    amount = request.form.get('amount')
    method = request.form.get('method')
    code = request.form.get('code')
    collected_by = request.form.get('collected_by')
    remarks = request.form.get('remarks')

    success, message = TuitionService.add_payment(fee_id, amount, method, code, collected_by, remarks)
    if success:
        flash(message, 'success')
        return redirect(url_for('tuitions.view', fee_id = fee_id))
    else:
        flash(message if isinstance(message, str) else ', '.join(message), 'danger')
        return redirect(url_for('tuitions.view', fee_id = fee_id))
    
@tuitions_bp.route('/add_tuition', methods=["GET","POST"])
def add_tuition():
    student_id = request.form.get('student_id')
    semester = request.form.get('semester')
    academic_year = request.form.get('academic_year')
    total_amount = request.form.get('total_amount')

    success, message = TuitionService.add_tuition(student_id, semester, academic_year, total_amount)
    if success:
        flash(message, 'success')
        return redirect(url_for('tuitions.list'))
    else:
        flash(message if isinstance(message, str) else ', '.join(message), 'danger')
        return redirect(url_for('tuitions.list'))
