"""Test related queries"""


SELECT_QUESTION_BLOCK_JSON_BY_ID = """
    SELECT JSON_OBJECT(
        'question_id', q.id,
        'question_content', q.content,
        'answer_list', JSON_ARRAYAGG(a.content)
    ) AS question_block_json
    FROM toeicapp_question q
    JOIN toeicapp_answer a ON a.question_id = q.id
    WHERE q.id = %s
    GROUP BY q.id, q.content;
"""

SELECT_QUESTION_EXPLAIN_BLOCK_JSON_BY_ID = """
    SELECT JSON_OBJECT(
        'question_id', q.id,
        'question_content', q.content,
        'answer_list', JSON_ARRAYAGG(
            JSON_OBJECT(
                'answer_content', a.content,
                'is_correct', a.is_correct
            )
        )
    ) AS question_explain_block_json
    FROM toeicapp_question q
    JOIN toeicapp_answer a ON a.question_id = q.id
    WHERE q.id = %s
    GROUP BY q.id, q.content;
"""

SELECT_QUESTION_TRANSLATE_JSON = """
    SELECT question_translate_json
    FROM toeicapp_question
    WHERE id = %s;
"""

SELECT_QUESTION_EXPLAIN_JSON = """
    SELECT question_explain_json
    FROM toeicapp_question
    WHERE id = %s;
"""

UPDATE_QUESTION_TRANSLATE_JSON_SCRIPT = """
    UPDATE toeicapp_question
    SET question_translate_json = %s
    WHERE id = %s;
"""

UPDATE_QUESTION_EXPLAIN_JSON_SCRIPT = """
    UPDATE toeicapp_question
    SET question_explain_json = %s
    WHERE id = %s;
"""

SELECT_PART_AUDIO_URL = """
    SELECT p.audio_url 
    FROM toeicapp_part p
    JOIN toeicapp_testpart tp ON p.id = tp.part_id
    WHERE tp.test_id =  %s 
    AND tp.part_id =  %s 
    AND p.part_order NOT IN ('Part 5', 'Part 6', 'Part 7');
"""


SELECT_BASE64_IMAGE_BY_MEDIA_ID = """
SELECT paragrap_main FROM toeicapp_media WHERE id = %s
"""


SELECT_AUDIO_SCRIPT_BY_MEDIA_ID = """
SELECT audio_script FROM toeicapp_media WHERE id = %s
"""

