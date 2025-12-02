# Student Management System

A comprehensive student management application built with Flask and MySQL.

## Features

- Student Management (Create, Read, Update, Delete)
- Instructor Management
- Course Management
- Search and Filter functionality
- Validation and error handling
- Modular architecture with Services and Models

## Project Structure

```
student_management/
├── main.py                 # Entry point
├── app/
│   ├── __init__.py        # Flask app factory
│   ├── config.py          # Configuration
│   ├── connection.py      # Database connection
│   ├── models/            # Data access layer
│   │   ├── student_model.py
│   │   ├── instructor_model.py
│   │   └── course_model.py
│   ├── services/          # Business logic layer
│   │   ├── student_service.py
│   │   ├── instructor_service.py
│   │   └── course_service.py
│   ├── routes/            # API routes
│   │   ├── students.py
│   │   ├── instructors.py
│   │   └── courses.py
│   ├── utils/
│   │   └── validators.py
│   ├── templates/         # HTML templates
│   │   ├── base.html
│   │   ├── students/
│   │   ├── instructors/
│   │   └── courses/
│   └── static/            # CSS, JS, images
├── database/
│   ├── scheme.sql
│   └── seed.sql
├── .env                   # Environment variables
└── requirements.txt       # Dependencies
```

## Installation

1. Clone or download the project
2. Create a Python virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database:
   - Create a MySQL database named `school_db`
   - Run `database/scheme.sql` to create tables
   - Optionally run `database/seed.sql` for sample data

5. Update `.env` file with your database credentials

## Running the Application

```bash
python main.py
```

The application will run at `http://localhost:5000`

## Database Setup

```sql
-- Create database
CREATE DATABASE school_db;

-- Run the schema file
source database/scheme.sql;

-- Run the seed file (optional)
source database/seed.sql;
```

## Architecture

- **Models**: Direct database access using MySQL connector
- **Services**: Business logic and validation
- **Routes**: Flask blueprints for HTTP endpoints
- **Templates**: Jinja2 templates for rendering HTML
- **Config**: Environment-based configuration

## API Endpoints

### Students
- `GET /students/` - List all students
- `GET /students/view/<id>` - View student details
- `GET /students/create` - Show create form
- `POST /students/create` - Create student
- `GET /students/update/<id>` - Show update form
- `POST /students/update/<id>` - Update student
- `POST /students/delete/<id>` - Delete student
- `POST /students/search` - Search students

### Instructors
- `GET /instructors/` - List all instructors
- `GET /instructors/create` - Show create form
- `POST /instructors/create` - Create instructor
- `GET /instructors/update/<id>` - Show update form
- `POST /instructors/update/<id>` - Update instructor
- `POST /instructors/delete/<id>` - Delete instructor
- `POST /instructors/search` - Search instructors

### Courses
- `GET /courses/` - List all courses
- `GET /courses/create` - Show create form
- `POST /courses/create` - Create course
- `GET /courses/update/<id>` - Show update form
- `POST /courses/update/<id>` - Update course
- `POST /courses/delete/<id>` - Delete course
- `POST /courses/search` - Search courses

## License

2025 NEU Student Management System
