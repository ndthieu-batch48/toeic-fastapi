"""Test related queries"""


SELECT_QUES_BLOCK_JSON_BY_ID = """
    SELECT JSON_OBJECT(
        'ques_id', q.id,
        'ques_content', q.content,
        'ans_list', JSON_ARRAYAGG(a.content)
    ) AS ques_block_json
    FROM toeicapp_question q
    JOIN toeicapp_answer a ON a.question_id = q.id
    WHERE q.id = %s
    GROUP BY q.id, q.content;
"""


UPDATE_TRANS_SCRIPT = """
    UPDATE toeic.toeicapp_media 
    SET translate_script = %s 
    WHERE id = %s
"""


UPDATE_EXPLAIN_QUES = """
    UPDATE toeic.toeicapp_media
    SET explain_question = %s
    WHERE id = %s
"""


SELECT_PART_AUDIO_URL = """
    SELECT p.audio_url 
    FROM toeicapp_part p
    JOIN toeicapp_testpart tp ON p.id = tp.part_id
    WHERE tp.test_id =  %s 
    AND tp.part_id =  %s 
    AND p.part_order NOT IN ('Part 5', 'Part 6', 'Part 7');
"""


SELECT_BASE64_IMAGE_BY_TEST_ID = """
select * from toeicapp_media where id = %s
"""

