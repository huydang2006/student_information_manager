-- VIEWS
USE school_db;
-- v_students_by_program
CREATE OR REPLACE VIEW v_students_by_program AS
SELECT
    p.program_id,
    p.program_name,
    s.student_id,
    s.full_name AS student_name,
    s.enrollment_year
FROM program p
JOIN student s ON s.program_id = p.program_id
WHERE p.is_deleted = 0
  AND s.is_deleted = 0
ORDER BY p.program_id, s.enrollment_year, s.full_name;

-- v_outstanding_tuition
CREATE OR REPLACE VIEW v_outstanding_tuition AS
SELECT
    tf.student_id,
    s.full_name AS student_name,
    tf.academic_year,
    tf.semester,
    tf.total_amount,
    tf.amount_paid,
    (tf.total_amount - tf.amount_paid) AS remaining_amount,
    CASE
      WHEN tf.amount_paid >= tf.total_amount THEN 'Fully Paid'
      WHEN tf.amount_paid > 0 AND tf.amount_paid < tf.total_amount THEN 'Partially Paid'
      ELSE 'Unpaid'
    END AS payment_status
FROM tuition_fee tf
JOIN student s ON s.student_id = tf.student_id
WHERE tf.is_deleted = 0
  AND s.is_deleted = 0
ORDER BY tf.academic_year DESC, tf.semester, s.full_name;

-- v_course_performance
CREATE OR REPLACE VIEW v_course_performance AS
SELECT
    c.course_id,
    c.course_name,
    COUNT(e.enrollment_id) AS num_students,
    ROUND(AVG(e.grade), 2) AS avg_grade,
    CASE
        WHEN COUNT(e.enrollment_id) = 0 THEN 0.00
        ELSE ROUND(
            100.0 * SUM(CASE WHEN e.grade IS NOT NULL AND e.grade >= 4.0 THEN 1 ELSE 0 END)
            / COUNT(e.enrollment_id),
            2
        )
    END AS pass_rate
FROM course c
LEFT JOIN enrollment e
    ON e.course_id = c.course_id
    AND e.is_deleted = 0
    AND e.status IN ('Enrolled','Completed','Withdrawn')
WHERE c.is_deleted = 0
GROUP BY c.course_id, c.course_name
ORDER BY c.course_id;
