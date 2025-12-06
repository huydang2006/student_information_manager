-- schema.sql 
-- CREATE DATABASE
CREATE DATABASE IF NOT EXISTS school_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE school_db;

-- DROP EXISTING TABLES TO AVOID CONFLICTS
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS payment;
DROP TABLE IF EXISTS tuition_fee;
DROP TABLE IF EXISTS advisor_assignment;
DROP TABLE IF EXISTS enrollment;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS program;
DROP TABLE IF EXISTS instructor;
DROP TABLE IF EXISTS student;

SET FOREIGN_KEY_CHECKS = 1;

-- TABLES
-- PROGRAMS
CREATE TABLE program (
    program_id INT AUTO_INCREMENT PRIMARY KEY,
    program_name VARCHAR(100) NOT NULL UNIQUE,
    department VARCHAR(100),
    duration_years INT UNSIGNED DEFAULT 4,
    degree_type ENUM('Bachelor','Master','PhD') DEFAULT 'Bachelor',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- STUDENTS
CREATE TABLE student (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender ENUM('Male','Female','Other') NOT NULL DEFAULT 'Other',
    email VARCHAR(100) UNIQUE,
    phone_number VARCHAR(50) DEFAULT NULL,
    address VARCHAR(255) DEFAULT NULL,
    program_id INT,
    enrollment_year YEAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_student_program
      FOREIGN KEY (program_id) REFERENCES program(program_id)
      ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- INSTRUCTORS
CREATE TABLE instructor (
    instructor_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    specialization VARCHAR(255),
    office_location VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- COURSES
CREATE TABLE course (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    credit_hours INT UNSIGNED DEFAULT 3,
    semester_offered ENUM('Spring','Summer','Fall') DEFAULT 'Spring',
    program_id INT DEFAULT NULL,
    instructor_id INT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_course_program
      FOREIGN KEY (program_id) REFERENCES program(program_id)
      ON DELETE SET NULL ON UPDATE CASCADE,
	CONSTRAINT fk_course_instructor
      FOREIGN KEY (instructor_id) REFERENCES instructor(instructor_id)
      ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ENROLLMENTS
CREATE TABLE enrollment (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    semester ENUM('Spring','Summer','Fall') DEFAULT 'Spring',
    academic_year YEAR,
    grade DECIMAL(5,2) DEFAULT NULL,
    status ENUM('Enrolled','Completed','Withdrawn') DEFAULT 'Enrolled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE(student_id, course_id, semester, academic_year),
    CONSTRAINT fk_enrollment_student
      FOREIGN KEY (student_id) REFERENCES student(student_id)
      ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_enrollment_course
      FOREIGN KEY (course_id) REFERENCES course(course_id)
      ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- TUITION FEES
CREATE TABLE tuition_fee (
    fee_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    academic_year YEAR,
    semester ENUM('Spring','Summer','Fall') DEFAULT 'Spring',
    total_amount DECIMAL(10,2) NOT NULL,
    amount_paid DECIMAL(10,2) DEFAULT 0,
    payment_status ENUM('Unpaid','Partially Paid','Fully Paid') DEFAULT 'Unpaid',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CHECK (amount_paid >= 0 AND total_amount >= 0),
    CONSTRAINT fk_fee_student
      FOREIGN KEY (student_id) REFERENCES student(student_id)
      ON DELETE CASCADE ON UPDATE CASCADE,
     UNIQUE(student_id, academic_year, semester)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- PAYMENTS
CREATE TABLE payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    fee_id INT NOT NULL,
    payment_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    amount DECIMAL(10,2) NOT NULL,
    payment_method ENUM('Cash','Bank Transfer','Card') DEFAULT 'Cash',
    transaction_code VARCHAR(100) DEFAULT NULL,
    collected_by VARCHAR(100) DEFAULT NULL,
    remarks VARCHAR(255),
    CHECK (amount > 0),
    CONSTRAINT fk_payment_fee
      FOREIGN KEY (fee_id) REFERENCES tuition_fee(fee_id)
      ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ADVISOR ASSIGNMENTS
CREATE TABLE advisor_assignment (
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,
    instructor_id INT NOT NULL,
    student_id INT NOT NULL,
    assigned_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE(student_id),
    CONSTRAINT fk_advisor_instructor
      FOREIGN KEY (instructor_id) REFERENCES instructor(instructor_id)
      ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_advisor_student
      FOREIGN KEY (student_id) REFERENCES student(student_id)
      ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

