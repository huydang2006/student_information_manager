# app/services/course_service.py
from app.models.course_model import Course
from app.utils.validators import validate_course_data


class CourseService:
    """Business logic for course operations"""

    @staticmethod
    def get_all_courses():
        """Get all courses"""
        return Course.get_all()

    @staticmethod
    def get_course_by_id(course_id):
        """Get a specific course"""
        return Course.get_by_id(course_id)

    @staticmethod
    def search_courses(course_id=None, name=None, program_id=None):
        """Search courses with filters"""
        return Course.search(course_id, name, program_id)

    @staticmethod
    def create_course(data):
        """Create a new course with validation"""
        # Validate data
        errors = validate_course_data(data)
        if errors:
            return False, errors

        # Check if course code exists
        if Course.code_exists(data.get('course_code')):
            return False, ["Course code already exists"]

        # Create course
        Course.create(
            course_name=data.get('course_name'),
            course_code=data.get('course_code'),
            program_id=data.get('program_id'),
            credits=data.get('credits'),
            description=data.get('description')
        )
        return True, "Course created successfully"

    @staticmethod
    def update_course(course_id, data):
        """Update course with validation"""
        course = Course.get_by_id(course_id)
        if not course:
            return False, "Course not found"

        # Validate data
        errors = validate_course_data(data, is_update=True)
        if errors:
            return False, errors

        # Check if new course code exists (if code is being changed)
        if 'course_code' in data and data['course_code'] != course.get('course_code'):
            if Course.code_exists(data.get('course_code')):
                return False, ["Course code already exists"]

        # Update course
        Course.update(course_id, **data)
        return True, "Course updated successfully"

    @staticmethod
    def delete_course(course_id):
        """Delete a course"""
        course = Course.get_by_id(course_id)
        if not course:
            return False, "Course not found"

        Course.delete(course_id)
        return True, "Course deleted successfully"
