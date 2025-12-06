# app/services/program_service.py
from app.models.program_model import Program
from app.models.course_model import Course
from app.utils.validators import validate_program_data


class ProgramService:
    """Business logic for program operations"""

    @staticmethod
    def get_all_programs():
        """Get all programs"""
        return Program.get_all()

    @staticmethod
    def get_program_by_id(program_id):
        """Get a specific program"""
        return Program.get_by_id(program_id)

    @staticmethod
    def search_programs(program_id=None, name=None):
        """Search courses with filters"""
        return Program.search(program_id, name)

    @staticmethod
    def create_program(data):
        """Create a new program with validation"""
        # Validate data
        errors = validate_program_data(data)
        if errors:
            return False, errors
        
        if Program.name_exists(data.get('program_name')):
            return False, ["Name is already exists"]

        # Create course
        Program.create(
            program_name=data.get('program_name'),
            department=data.get('department'),
            duration_year=data.get('duration_year'),
            degree_type=data.get('degree_type')
        )
        return True, "Program created successfully"

    @staticmethod
    def create_course(data):
        """Create a new program with validation"""
        # Validate data
        errors = validate_program_data(data)
        if errors:
            return False, errors

        # Create course
        Program.create(
            course_name=data.get('course_name'),
            course_code=data.get('course_code'),
            program_id=data.get('program_id'),
            credits=data.get('credits'),
            description=data.get('description')
        )
        return True, "Course created successfully"

    @staticmethod
    def delete_program(program_id):
        """Delete a course"""
        program = Program.get_by_id(program_id)
        if not program:
            return False, "Program not found"

        Program.delete(program_id)
        return True, "Program deleted successfully"

    @staticmethod
    def update_program(program_id, data):
        """Update program with validation"""
        program = Program.get_by_id(program_id)
        if not program:
            return False, "Program not found"

        # Validate data
        errors = validate_program_data(data, is_update=True)
        if errors:
            return False, errors

        # Update student
        Program.update(program_id, **data)
        return True, "Program updated successfully"
    
    @staticmethod
    def update_course(course_id, data):
        """Update program with validation"""
        # Validate data
        # errors = validate_program_data(data, is_update=True)
        # if errors:
        #     return False, errors

        # Update student
        Program.updatecourse(course_id, **data)
        return True, "Course updated successfully"