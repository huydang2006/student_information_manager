# app/utils/validators.py
import re
from datetime import datetime


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


# def validate_phone(phone):
#     """Validate phone number format"""
#     pattern = r'^[\d\s\-\+\(\)]{10,}$'
#     return re.match(pattern, phone) is not None if phone else True


def validate_date(date_str):
    """Validate date format (YYYY-MM-DD) or empty"""
    if not date_str or date_str.strip() == '':
        return True  # Empty dates are allowed for optional fields
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except (ValueError, TypeError):
        return False


def validate_student_data(data, is_update=False):
    """Validate student data"""
    errors = []

    if not is_update:
        # Required fields for creation
        if not data.get('full_name'):
            errors.append("Full name is required")
        if not data.get('email'):
            errors.append("Email is required")
        if not data.get('program_id'):
            errors.append("Program is required")
        if not data.get('enrollment_year'):
            errors.append("Enrollment year is required")

    # Conditional validations
    if data.get('email') and not validate_email(data.get('email')):
        errors.append("Invalid email format")

    # if data.get('phone_number') and not validate_phone(data.get('phone_number')):
    #     errors.append("Invalid phone number format")

    if data.get('date_of_birth') and not validate_date(data.get('date_of_birth')):
        errors.append("Invalid date format (use YYYY-MM-DD)")

    if data.get('enrollment_year'):
        try:
            year = int(data.get('enrollment_year'))
            if year < 2000 or year > datetime.now().year:
                errors.append(f"Enrollment year must be between 2000 and {datetime.now().year}")
        except (ValueError, TypeError):
            errors.append("Enrollment year must be a number")

    return errors


def validate_instructor_data(data, is_update=False):
    """Validate instructor data"""
    errors = []

    if not is_update:
        # Required fields for creation
        if not data.get('full_name'):
            errors.append("Full name is required")
        if not data.get('email'):
            errors.append("Email is required")

    # Conditional validations
    if data.get('email') and not validate_email(data.get('email')):
        errors.append("Invalid email format")

    return errors


def validate_program_data(data, is_update=False):
    """Validate program data"""
    errors = []

    if not is_update:
        # Required fields for creation
        if not data.get('program_name'):
            errors.append("Program name is required")
        if not data.get('department'):
            errors.append("department")
        if not data.get('degree_type'):
            errors.append("Degree Type is required")

    # Conditional validations
    if data.get('duration_years'):
        try:
            credits = int(data.get('duration_years'))
            if credits < 1 or credits > 8:
                errors.append("Duration Years must be between 3 and 8")
        except (ValueError, TypeError):
            errors.append("Duration Years must be a number")

    return errors

def validate_enrollment_data(data, is_update=False):
    """Validate program data"""
    errors = []

    # if not is_update:
    #     # Required fields for creation
    #     if not data.get('program_name'):
    #         errors.append("Program name is required")
    #     if not data.get('department'):
    #         errors.append("department")
    #     if not data.get('degree_type'):
    #         errors.append("Degree Type is required")

    # Conditional validations
    if data.get('academic_year'):
        credits = int(data.get('academic_year'))
        if credits < 2024 or credits > 2050:
            errors.append("Duration Years must be between 2024 and 2050")

    return errors
