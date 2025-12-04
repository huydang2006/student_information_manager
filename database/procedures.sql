-- STORED PROCEDURES
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
    -- check student exists and is not deleted
    SELECT COUNT(*) INTO v_exists_student
    FROM student
    WHERE student_id = p_student_id AND is_deleted = 0;
    IF v_exists_student = 0 THEN
        SELECT 0 AS success, CONCAT('Failure: student_id ', p_student_id, ' does not exist or is deleted.') AS message;
        LEAVE main_block;
    END IF;
    -- check course exists and is not deleted
    SELECT COUNT(*) INTO v_exists_course
    FROM course
    WHERE course_id = p_course_id AND is_deleted = 0;
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
      AND academic_year = p_academic_year
      AND is_deleted = 0;
    IF v_already_enrolled > 0 THEN
        SELECT 0 AS success, CONCAT('Failure: student already enrolled for ', p_semester, ' ', p_academic_year, '.') AS message;
        LEAVE main_block;
    END IF;
    -- Insert enrollment
    INSERT INTO enrollment (student_id, course_id, semester, academic_year, enrolled_date, status)
    VALUES (p_student_id, p_course_id, p_semester, p_academic_year, CURRENT_TIMESTAMP, 'Enrolled');
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
    -- Revenue per program
    SELECT
        pr.program_id,
        pr.program_name,
        COUNT(DISTINCT tf.student_id) AS num_students_billed,
        ROUND(IFNULL(SUM(pay.amount),0), 2) AS total_revenue_collected
    FROM tuition_fee tf
    JOIN student s ON s.student_id = tf.student_id AND s.is_deleted = 0
    LEFT JOIN program pr ON pr.program_id = s.program_id AND pr.is_deleted = 0
    LEFT JOIN payment pay ON pay.fee_id = tf.fee_id AND pay.is_deleted = 0
    WHERE tf.is_deleted = 0
      AND tf.academic_year = p_academic_year
      AND tf.semester = p_semester
    GROUP BY pr.program_id, pr.program_name
    ORDER BY total_revenue_collected DESC;
    -- Overall totals
    SELECT
        NULL AS program_id,
        'ALL PROGRAMS' AS program_name,
        COUNT(DISTINCT tf.student_id) AS num_students_billed,
        ROUND(IFNULL(SUM(pay.amount),0), 2) AS total_revenue_collected
    FROM tuition_fee tf
    LEFT JOIN payment pay ON pay.fee_id = tf.fee_id AND pay.is_deleted = 0
    WHERE tf.is_deleted = 0
      AND tf.academic_year = p_academic_year
      AND tf.semester = p_semester;
END$$
DELIMITER ;