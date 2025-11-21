"""History and progress related queries"""

INSERT_HISTORY = """
    INSERT INTO toeicapp_history (dataprogress, type, part, time, test_id, user_id, create_at, status, time_left)
    VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s, NULL)
"""

UPDATE_HISTORY_BY_USER = """
    UPDATE toeicapp_history
    SET dataprogress = %s,
        type = %s,
        part = %s,
        time = %s,
        create_at = NOW(),
        status = %s,
        time_left = NULL
    WHERE user_id = %s AND test_id = %s;
"""


SELECT_HISTORY_BY_STATUS = """
    SELECT 
        id, 
        dataprogress AS data_progress,
        type, 
        part AS part_id_list,
        time AS duration, 
        test_id,
        user_id,
        create_at,
        status 
    FROM toeicapp_history 
    WHERE user_id = %s AND test_id = %s AND status = %s 
    ORDER BY create_at DESC 
"""


SELECT_SUBMIT_HISTORY_BY_USER = """
    SELECT 
        id, 
        dataprogress AS data_progress,
        type, 
        part AS part_id_list,
        time AS duration, 
        test_id,
        user_id,
        create_at,
        status 
    FROM toeicapp_history 
    WHERE user_id = %s 
    AND status = 'submit'
    ORDER BY create_at DESC
    LIMIT 10
"""


SELECT_HISTORY_BY_ID = """
    SELECT 
        id, 
        dataprogress AS data_progress,
        type, 
        part AS part_id_list,
        time AS duration, 
        test_id,
        user_id,
        create_at,
        status 
    FROM toeicapp_history 
    WHERE id = %s
"""


GET_TITLE_OF_TEST = "SELECT title FROM toeicapp_test WHERE id = %s"


def select_count_correct_incorrect_by_answer_id(answer_id_list):
    placeholders = ", ".join(["%s"] * len(answer_id_list))
    return f"""
        SELECT
            SUM(CASE WHEN a.is_correct = 1 THEN 1 ELSE 0 END) AS correct_count,
            SUM(CASE WHEN a.is_correct = 0 THEN 1 ELSE 0 END) AS incorrect_count
        FROM toeicapp_answer a
        WHERE a.id IN ({placeholders});
    """


SELECT_CALCULATE_DATA_PROGRESS_RESULT_BY_HISTORY_ID = """
    SELECT
        COALESCE(SUM(CASE WHEN a.is_correct = 1 THEN 1 ELSE 0 END), 0) AS correct_count,
        COALESCE(SUM(CASE WHEN a.is_correct = 0 THEN 1 ELSE 0 END), 0) AS incorrect_count,
        COALESCE(SUM(CASE WHEN a.is_correct = 1 AND q.question_number BETWEEN 1 AND 100
                THEN 1 ELSE 0 END), 0) AS correct_listening,
        COALESCE(SUM(CASE WHEN a.is_correct = 1 AND q.question_number >= 101
                THEN 1 ELSE 0 END), 0) AS correct_reading
    FROM toeicapp_history h
    JOIN JSON_TABLE(
        JSON_KEYS(h.dataprogress),
        '$[*]' COLUMNS(question_id VARCHAR(64) PATH '$')
    ) AS k
    JOIN toeicapp_answer a 
        ON a.id = JSON_UNQUOTE(
                    JSON_EXTRACT(h.dataprogress, CONCAT('$."', k.question_id, '"'))
                )
    JOIN toeicapp_question q ON a.question_id = q.id
    WHERE h.id = %s;
"""


SELECT_CALCULATE_CORRECT_ANSWER_BY_HISTORY_ID = """
    SELECT
        COALESCE(SUM(CASE WHEN a.is_correct = 1 THEN 1 ELSE 0 END), 0) AS correct_count
    FROM toeicapp_history h
    JOIN JSON_TABLE(
        JSON_KEYS(h.dataprogress),
        '$[*]' COLUMNS(question_id VARCHAR(64) PATH '$')
    ) AS k
    JOIN toeicapp_answer a 
        ON a.id = JSON_UNQUOTE(
                    JSON_EXTRACT(h.dataprogress, CONCAT('$."', k.question_id, '"'))
                )
    WHERE h.id = %s;
"""


SELECT_COUNT_QUESTIONS_BY_TEST = """
    SELECT count(q.id) AS question_by_test_count
    FROM toeicapp_testpart tp
    JOIN toeicapp_question q ON tp.part_id = q.part_id
    WHERE test_id = %s;
"""


def select_multiple_part_order_by_part_id(part_id_list):
    placeholders = ", ".join(["%s"] * len(part_id_list))
    return f"""
        SELECT part_order 
        FROM toeicapp_part 
        WHERE id IN ({placeholders});
    """


def select_count_questions_by_multiple_part(part_id_list):
    placeholders = ", ".join(["%s"] * len(part_id_list))
    return f"""
        SELECT COUNT(q.id) AS question_by_multiple_part_count
        FROM toeicapp_testpart tp
        JOIN toeicapp_part p ON tp.part_id = p.id
        JOIN toeicapp_question q ON tp.part_id = q.part_id
        WHERE test_id = %s
        AND p.id IN ({placeholders});
    """