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


UPDATE_TRANSLATE_SCRIPT = """
    UPDATE toeic.toeicapp_media 
    SET translate_script = %s 
    WHERE id = %s
"""


UPDATE_EXPLAIN_QUESTION = """
    UPDATE toeic.toeicapp_media
    SET explain_question = %s
    WHERE id = %s
"""


