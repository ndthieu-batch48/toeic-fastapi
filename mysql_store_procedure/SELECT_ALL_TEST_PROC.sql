DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `SELECT_ALL_TEST_PROC`(
    OUT pJSON_LIST_RESULT JSON
)
BEGIN
    WITH question_counts AS (
        SELECT 
            tp.test_id,
            q.part_id,
            COUNT(q.id) AS total_question
        FROM toeicapp_question q
        JOIN toeicapp_testpart tp ON q.part_id = tp.part_id
        GROUP BY tp.test_id, q.part_id
    ),
    test_data AS (
        SELECT 
            JSON_OBJECT(
                'test_id', t.id, 
                'test_title', t.title, 
                'test_description', t.description, 
                'test_duration', t.duration, 
                'part_list', JSON_ARRAYAGG(
                    JSON_OBJECT(
                        'part_id', p.id,
                        'part_order', p.part_order,
                        'part_title', p.title,
                        'total_question', COALESCE(qc.total_question, 0)
                    )
                )
            ) AS test_json
        FROM toeicapp_test t
        JOIN toeicapp_testpart tp ON tp.test_id = t.id
        JOIN toeicapp_part p ON tp.part_id = p.id
        LEFT JOIN question_counts qc 
        ON qc.test_id = t.id AND qc.part_id = p.id
        WHERE t.visible = 1
        GROUP BY t.id, t.title, t.description, t.duration
    )
    SELECT JSON_ARRAYAGG(test_json)
    INTO pJSON_LIST_RESULT
    FROM test_data;
END$$
DELIMITER ;