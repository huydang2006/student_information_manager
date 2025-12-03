# app/services/program_service.py
from app.models.program_model import Program
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

    # @staticmethod
    # def update_course(course_id, data):
    #     """Update course with validation"""
    #     course = Course.get_by_id(course_id)
    #     if not course:
    #         return False, "Course not found"

    #     # Validate data
    #     errors = validate_course_data(data, is_update=True)
    #     if errors:
    #         return False, errors

    #     # Check if new course code exists (if code is being changed)
    #     if 'course_code' in data and data['course_code'] != course.get('course_code'):
    #         if Course.code_exists(data.get('course_code')):
    #             return False, ["Course code already exists"]

    #     # Update course
    #     Course.update(course_id, **data)
    #     return True, "Course updated successfully"

    @staticmethod
    def delete_program(program_id):
        """Delete a course"""
        program = Program.get_by_id(program_id)
        if not program:
            return False, "Program not found"

        Program.delete(program_id)
        return True, "Program deleted successfully"
