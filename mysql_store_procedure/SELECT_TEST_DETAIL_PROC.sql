USE toeic;

CREATE PROCEDURE SELECT_TEST_DETAIL_PROC (
    IN pTEST_ID INT,
    OUT pJSON_RESULT JSON
)
BEGIN

    SELECT JSON_OBJECT(
        'part_list', JSON_ARRAYAGG(
            JSON_OBJECT(
                'part_id', p_id,
                'part_order', p_order,
                'part_title', p_title,
                'part_audio_url', p_audio_url,
                'media_question_list', media_question_list
            )
        )
    ) INTO pJSON_RESULT
    FROM (
        SELECT 
            p_id,
            p_order,
            p_title,
            p_audio_url,
            JSON_ARRAYAGG(
                JSON_OBJECT(
                    'media_question_id', m_id,
                    'media_question_name', m_media_name,
                    'media_question_main_paragraph', m_main_paragraph,
                    'media_question_audio_script', m_audio_script,
                    'question_list', question_list
                )
            ) AS media_question_list
        FROM (
            SELECT 
                p.id AS p_id,
                p.part_order AS p_order,
                p.title AS p_title,
                p.audio_url AS p_audio_url,
                m.id AS m_id,
                m.media_name AS m_media_name,
                m.paragrap_main AS m_main_paragraph,
                m.audio_script AS m_audio_script,
                JSON_ARRAYAGG(
                    JSON_OBJECT(
                        'question_id', q.id,
                        'question_number', q.question_number,
                        'question_content', q.content,
                        'answer_list', (
                            SELECT JSON_ARRAYAGG(
                                JSON_OBJECT(
                                    'answer_id', a.id,
                                    'is_correct', a.is_correct,
                                    'content', a.content
                                )
                            )
                            FROM toeicapp_answer a
                            WHERE a.question_id = q.id
                        )
                    )
                ) AS question_list
            FROM toeicapp_part p
            JOIN toeicapp_testpart tp ON tp.part_id = p.id
            JOIN toeicapp_question q ON q.part_id = p.id
            JOIN toeicapp_media m ON q.media_group_id = m.id
            WHERE tp.test_id = pTEST_ID
            GROUP BY p.id, m.id
        ) tmp
        GROUP BY tmp.p_id, tmp.p_order, tmp.p_title, tmp.p_audio_url
    ) final;
END
