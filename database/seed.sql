-- Sample Data for Student Management System

-- Insert Sample Programs
INSERT INTO program (program_name, description) VALUES
('Computer Science', 'Bachelor of Science in Computer Science'),
('Business Administration', 'Bachelor of Business Administration'),
('Information Technology', 'Bachelor of Information Technology'),
('Engineering', 'Bachelor of Engineering'),
('Finance', 'Bachelor of Finance');

-- Insert Sample Students
INSERT INTO student (full_name, email, phone_number, address, date_of_birth, gender, program_id, enrollment_year) VALUES
('Nguyen Van A', 'nguyenvana@student.neu.edu', '0901234567', '123 Main St, Ha Noi', '2002-05-15', 'Male', 1, 2022),
('Tran Thi B', 'tranthib@student.neu.edu', '0912345678', '456 Oak Ave, Ho Chi Minh', '2003-08-22', 'Female', 2, 2023),
('Pham Van C', 'phamvanc@student.neu.edu', '0923456789', '789 Pine Rd, Da Nang', '2002-03-10', 'Male', 1, 2022),
('Le Thi D', 'lethid@student.neu.edu', '0934567890', '321 Elm St, Ha Noi', '2003-11-05', 'Female', 3, 2023),
('Hoang Van E', 'hoangvane@student.neu.edu', '0945678901', '654 Maple Dr, Ho Chi Minh', '2002-07-30', 'Male', 4, 2022);

-- Insert Sample Instructors
INSERT INTO instructor (full_name, email, specialization, office_location) VALUES
('Dr. Dang Xuan Phu', 'dang.phu@neu.edu', 'Software Engineering', 'Building A, Room 201'),
('Prof. Truong Minh Tuan', 'truong.tuan@neu.edu', 'Database Systems', 'Building B, Room 305'),
('Dr. Le Van Hai', 'le.hai@neu.edu', 'Web Development', 'Building A, Room 215'),
('Prof. Nguyen Thanh Tuan', 'nguyen.tuan@neu.edu', 'Business Management', 'Building C, Room 101'),
('Dr. Pham Duc Minh', 'pham.minh@neu.edu', 'Network Administration', 'Building B, Room 212');

-- Insert Sample Courses
INSERT INTO course (course_name, course_code, program_id, credits, description) VALUES
('Introduction to Programming', 'CS101', 1, 3, 'Basics of programming using Python'),
('Database Design', 'CS201', 1, 4, 'Learn database design and SQL'),
('Web Development Fundamentals', 'IT101', 3, 3, 'HTML, CSS, JavaScript basics'),
('Business Communication', 'BA101', 2, 2, 'Effective communication in business'),
('Financial Accounting', 'FI101', 5, 4, 'Introduction to financial accounting'),
('Data Structures', 'CS102', 1, 4, 'Advanced data structures and algorithms'),
('Project Management', 'BA201', 2, 3, 'Project management principles and techniques');

-- Insert Sample Enrollments
INSERT INTO enrollment (student_id, course_id, grade, status) VALUES
(1, 1, 'A', 'Completed'),
(1, 2, 'B+', 'Completed'),
(2, 4, 'A', 'Completed'),
(2, 5, 'A-', 'Active'),
(3, 1, 'B', 'Completed'),
(3, 6, 'B+', 'Active'),
(4, 3, 'A', 'Completed'),
(4, 7, 'B', 'Active'),
(5, 1, 'A', 'Completed'),
(5, 2, 'A-', 'Active');
