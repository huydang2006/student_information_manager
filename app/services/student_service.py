# app/services/student_service.py
from app.models.student_model import Student
from app.utils.validators import validate_student_data, validate_email


class StudentService:
    """Business logic for student operations"""

    @staticmethod
    def get_all_students():
        """Get all students"""
        return Student.get_all()

    @staticmethod
    def get_student_by_id(student_id):
        """Get a specific student"""
        return Student.get_by_id(student_id)

    @staticmethod
    def search_students(student_id=None, name=None, program_id=None, enrollment_year=None):
        """Search students with filters"""
        return Student.search(student_id, name, program_id, enrollment_year)

    @staticmethod
    def create_student(data):
        """Create a new student with validation"""
        # Validate data
        errors = validate_student_data(data)
        if errors:
            return False, errors

        # Check if email exists
        if Student.email_exists(data.get('email')):
            return False, ["Email already exists"]

        # Create student
        Student.create(
            full_name=data.get('full_name'),
            email=data.get('email'),
            phone_number=data.get('phone_number'),
            address=data.get('address'),
            date_of_birth=data.get('date_of_birth'),
            gender=data.get('gender'),
            program_id=data.get('program_id'),
            enrollment_year=data.get('enrollment_year')
        )
        return True, "Student created successfully"

    @staticmethod
    def update_student(student_id, data):
        """Update student with validation"""
        student = Student.get_by_id(student_id)
        if not student:
            return False, "Student not found"

        # Validate data
        errors = validate_student_data(data, is_update=True)
        if errors:
            return False, errors

        # Check if new email exists (if email is being changed)
        if 'email' in data and data['email'] != student.get('email'):
            if Student.email_exists(data.get('email')):
                return False, ["Email already exists"]

        # Update student
        Student.update(student_id, **data)
        return True, "Student updated successfully"

    @staticmethod
    def delete_student(student_id):
        """Delete a student"""
        student = Student.get_by_id(student_id)
        if not student:
            return False, "Student not found"

        Student.delete(student_id)
        return True, "Student deleted successfully"
