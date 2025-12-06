# app/services/student_service.py
from app.models.student_model import Student
from app.utils.validators import validate_student_data, validate_email, validate_enrollment_data


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

        # Clean empty optional fields
        date_of_birth = data.get('date_of_birth')
        date_of_birth = None if not date_of_birth or date_of_birth.strip() == '' else date_of_birth
        
        phone_number = data.get('phone_number')
        phone_number = None if not phone_number or phone_number.strip() == '' else phone_number
        
        address = data.get('address')
        address = None if not address or address.strip() == '' else address

        # Create student
        Student.create(
            full_name=data.get('full_name'),
            email=data.get('email'),
            phone_number=phone_number,
            address=address,
            date_of_birth=date_of_birth,
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

        # Clean empty optional fields
        if 'date_of_birth' in data:
            data['date_of_birth'] = None if not data['date_of_birth'] or data['date_of_birth'].strip() == '' else data['date_of_birth']
        if 'phone_number' in data:
            data['phone_number'] = None if not data['phone_number'] or data['phone_number'].strip() == '' else data['phone_number']
        if 'address' in data:
            data['address'] = None if not data['address'] or data['address'].strip() == '' else data['address']

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
    
    @staticmethod
    def get_enrollments_student(student_id):
        student = Student.get_by_id(student_id)
        if not student:
            return False, "Student not found"
        
        return Student.get_enrollments(student_id)

    @staticmethod
    def delete_enrollment(enrollment_id):
        """Delete enrollment"""

        Student.deleteEnrollment(enrollment_id)
        return True, "Enrollment deleted successfully"
    
    @staticmethod
    def create_enrollment(data):
        """Create a new enrollment with validation"""
        # Validate data
        errors = validate_enrollment_data(data)
        if errors:
            return False, errors

        # # Clean empty optional fields
        # date_of_birth = data.get('date_of_birth')
        # date_of_birth = None if not date_of_birth or date_of_birth.strip() == '' else date_of_birth
        
        # phone_number = data.get('phone_number')
        # phone_number = None if not phone_number or phone_number.strip() == '' else phone_number
        
        # address = data.get('address')
        # address = None if not address or address.strip() == '' else address

        # Create enrollment
        Student.createEnrollment(
            student_id=data.get('student_id'),
            course_id=data.get('course_id'),
            semester=data.get('semester'),
            academic_year=data.get('academic_year'),
        )
        return True, "Enrollment added successfully"


    @staticmethod
    def update_enrollment(enrollment_id, academic_year, grade, status):
        Student.updateenrollment(enrollment_id, academic_year, grade, status)
        return True, "Enrollment updated successfully"
