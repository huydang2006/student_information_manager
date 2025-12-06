-- views.sql
USE school_db;

-- v_tuition_fee_summary
CREATE OR REPLACE VIEW v_tuition_fee_summary AS
SELECT 
    payment_status,
    COUNT(*) AS total_count
FROM tuition_fee
GROUP BY payment_status;

-- v_top_gpa
CREATE OR REPLACE VIEW v_top_gpa AS
SELECT 
    student_id,
    full_name,
    gpa
FROM (
    SELECT 
        s.student_id,
        s.full_name,
        ROUND(
            (SUM(e.grade * c.credit_hours) / SUM(c.credit_hours)) / 10 * 4,
            2
        ) AS gpa
    FROM student s
    JOIN enrollment e ON s.student_id = e.student_id
    JOIN course c ON e.course_id = c.course_id
    WHERE e.status = 'Completed'
      AND e.grade IS NOT NULL
    GROUP BY s.student_id, s.full_name
    HAVING gpa IS NOT NULL
    ORDER BY gpa DESC
    LIMIT 10
) AS sub;

-- v_grade_distribution
CREATE OR REPLACE VIEW v_grade_distribution AS
WITH ranges AS (
    SELECT 0 AS min_grade, 1 AS max_grade, '0–1' AS label UNION ALL
    SELECT 1, 2, '1–2' UNION ALL
    SELECT 2, 3, '2–3' UNION ALL
    SELECT 3, 4, '3–4' UNION ALL
    SELECT 4, 5, '4–5' UNION ALL
    SELECT 5, 6, '5–6' UNION ALL
    SELECT 6, 7, '6–7' UNION ALL
    SELECT 7, 8, '7–8' UNION ALL
    SELECT 8, 9, '8–9' UNION ALL
    SELECT 9, 10, '9–10'
)
SELECT 
    r.label AS grade_range,
    COUNT(e.grade) AS total_students
FROM ranges r
LEFT JOIN enrollment e 
    ON e.grade >= r.min_grade 
   AND e.grade < r.max_grade 
   AND e.grade IS NOT NULL
GROUP BY r.label, r.min_grade
ORDER BY r.min_grade;