-- procedures.sql
USE school_db;
DELIMITER $$

-- sp_register_course
DROP PROCEDURE IF EXISTS sp_register_course$$
CREATE PROCEDURE sp_register_course(
    IN p_student_id INT,
    IN p_course_id INT,
    IN p_semester VARCHAR(10),
    IN p_academic_year INT
)
main_block: BEGIN
    DECLARE v_exists_student INT;
    DECLARE v_exists_course INT;
    DECLARE v_already_enrolled INT;
    DECLARE v_enrollment_id INT;
    -- check student exists
    SELECT COUNT(*) INTO v_exists_student
    FROM student
    WHERE student_id = p_student_id;
    IF v_exists_student = 0 THEN
        SELECT 0 AS success, CONCAT('Failure: student_id ', p_student_id, ' does not exist or is deleted.') AS message;
        LEAVE main_block;
    END IF;
    -- check course exists
    SELECT COUNT(*) INTO v_exists_course
    FROM course
    WHERE course_id = p_course_id;
    IF v_exists_course = 0 THEN
        SELECT 0 AS success, CONCAT('Failure: course_id ', p_course_id, ' does not exist or is deleted.') AS message;
        LEAVE main_block;
    END IF;
    -- check duplicate enrollment
    SELECT COUNT(*) INTO v_already_enrolled
    FROM enrollment
    WHERE student_id = p_student_id
      AND course_id = p_course_id
      AND semester = p_semester
      AND academic_year = p_academic_year;
    IF v_already_enrolled > 0 THEN
        SELECT 0 AS success, CONCAT('Failure: student already enrolled for ', p_semester, ' ', p_academic_year, '.') AS message;
        LEAVE main_block;
    END IF;
    -- Insert enrollment
    INSERT INTO enrollment (student_id, course_id, semester, academic_year, status)
    VALUES (p_student_id, p_course_id, p_semester, p_academic_year, 'Enrolled');
    SET v_enrollment_id = LAST_INSERT_ID();
    SELECT 1 AS success, CONCAT('Success: enrolled, enrollment_id=', v_enrollment_id) AS message;
END main_block$$

-- sp_semester_revenue_report
DROP PROCEDURE IF EXISTS sp_semester_revenue_report$$
CREATE PROCEDURE sp_semester_revenue_report(
    IN p_academic_year INT,
    IN p_semester VARCHAR(10)
)
BEGIN
    SELECT
        COUNT(tf.fee_id) AS num_tuitions,
        ROUND(IFNULL(SUM(pay.amount), 0), 2) AS total_revenue_collected
    FROM tuition_fee tf
    LEFT JOIN payment pay ON pay.fee_id = tf.fee_id
    WHERE tf.academic_year = p_academic_year
      AND tf.semester = p_semester;
END$$

-- sp_courses_by_program
DROP PROCEDURE IF EXISTS sp_courses_by_program$$
CREATE PROCEDURE sp_courses_by_program(
    IN p_program_id INT
)
BEGIN
    SELECT 
        c.course_id,
        c.course_name,
        c.credit_hours,
        c.semester_offered,
        p.program_name,
        i.full_name AS instructor_name
    FROM course c
    LEFT JOIN program p ON c.program_id = p.program_id
    LEFT JOIN instructor i ON c.instructor_id = i.instructor_id
    WHERE c.program_id = p_program_id;
END$$

-- sp_enrollments_by_student
DROP PROCEDURE IF EXISTS sp_enrollments_by_student$$
CREATE PROCEDURE sp_enrollments_by_student(
    IN p_student_id INT
)
BEGIN
    SELECT
        e.enrollment_id,
        s.full_name AS student_name,
        c.course_name,
        e.semester,
        e.academic_year,
        e.grade,
        e.status
    FROM enrollment e
    INNER JOIN student s ON e.student_id = s.student_id
    INNER JOIN course c ON e.course_id = c.course_id
    WHERE e.student_id = p_student_id
    ORDER BY e.academic_year DESC, e.semester;
END$$

DELIMITER ;