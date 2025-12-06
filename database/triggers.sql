-- trigger.sql
DELIMITER $$

-- trg_before_payment_insert
DROP TRIGGER IF EXISTS trg_before_payment_insert$$
CREATE TRIGGER trg_before_payment_insert
BEFORE INSERT ON payment
FOR EACH ROW
BEGIN
    DECLARE v_status ENUM('Unpaid','Partially Paid','Fully Paid');

    -- Get current fee payment status
    SELECT payment_status INTO v_status
    FROM tuition_fee
    WHERE fee_id = NEW.fee_id;

    -- Block insert if already fully paid
    IF v_status = 'Fully Paid' THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Payment denied: Tuition fee already fully paid.';
    END IF;

END$$

-- trg_after_payment_insert
DROP TRIGGER IF EXISTS trg_after_payment_insert$$
CREATE TRIGGER trg_after_payment_insert
AFTER INSERT ON payment
FOR EACH ROW
BEGIN
    DECLARE v_total_paid DECIMAL(18,2);
    -- Recalculate total paid 
    SELECT IFNULL(SUM(amount), 0.00) INTO v_total_paid
    FROM payment
    WHERE fee_id = NEW.fee_id;
    -- Update tuition_fee.amount_paid and payment_status
    UPDATE tuition_fee
    SET amount_paid = v_total_paid,
        payment_status =
            CASE
                WHEN v_total_paid >= total_amount THEN 'Fully Paid'
                WHEN v_total_paid > 0 AND v_total_paid < total_amount THEN 'Partially Paid'
                ELSE 'Unpaid'
            END,
        updated_at = CURRENT_TIMESTAMP
    WHERE fee_id = NEW.fee_id;
END$$

DELIMITER ;