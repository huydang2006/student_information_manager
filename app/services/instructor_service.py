# app/services/instructor_service.py
from app.models.instructor_model import Instructor
from app.utils.validators import validate_instructor_data


class InstructorService:
    """Business logic for instructor operations"""

    @staticmethod
    def get_all_instructors():
        """Get all instructors"""
        return Instructor.get_all()

    @staticmethod
    def get_instructor_by_id(instructor_id):
        """Get a specific instructor"""
        return Instructor.get_by_id(instructor_id)

    @staticmethod
    def search_instructors(instructor_id=None, name=None, email=None):
        """Search instructors with filters"""
        return Instructor.search(instructor_id, name, email)

    @staticmethod
    def create_instructor(data):
        """Create a new instructor with validation"""
        # Validate data
        errors = validate_instructor_data(data)
        if errors:
            return False, errors

        # Check if email exists
        if Instructor.email_exists(data.get('email')):
            return False, ["Email already exists"]

        # Create instructor
        Instructor.create(
            full_name=data.get('full_name'),
            email=data.get('email'),
            specialization=data.get('specialization'),
            office_location=data.get('office_location')
        )
        return True, "Instructor created successfully"

    @staticmethod
    def update_instructor(instructor_id, data):
        """Update instructor with validation"""
        instructor = Instructor.get_by_id(instructor_id)
        if not instructor:
            return False, "Instructor not found"

        # Validate data
        errors = validate_instructor_data(data, is_update=True)
        if errors:
            return False, errors

        # Check if new email exists (if email is being changed)
        if 'email' in data and data['email'] != instructor.get('email'):
            if Instructor.email_exists(data.get('email')):
                return False, ["Email already exists"]

        # Update instructor
        Instructor.update(instructor_id, **data)
        return True, "Instructor updated successfully"

    @staticmethod
    def delete_instructor(instructor_id):
        """Delete an instructor"""
        instructor = Instructor.get_by_id(instructor_id)
        if not instructor:
            return False, "Instructor not found"

        Instructor.delete(instructor_id)
        return True, "Instructor deleted successfully"
