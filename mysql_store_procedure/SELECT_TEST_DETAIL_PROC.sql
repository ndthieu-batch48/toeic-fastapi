USE toeicapp;

DELIMITER $$
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
                'media_ques_list', media_ques_list
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
                    'media_ques_id', m_id,
                    'media_ques_name', m_media_name,
                    'media_ques_main_parag', m_parag_main,
                    'media_ques_audio_script', m_audio_script,
                    'media_ques_explain', m_explain_ques,
                    'media_ques_trans_script', m_trans_script,
                    'ques_list', ques_list
                )
            ) AS media_ques_list
        FROM (
            SELECT 
                p.id AS p_id,
                p.part_order AS p_order,
                p.title AS p_title,
                p.audio_url AS p_audio_url,
                m.id AS m_id,
                m.media_name AS m_media_name,
                m.paragrap_main AS m_parag_main,
                m.audio_script AS m_audio_script,
                m.explain_question AS m_explain_ques,
                m.translate_script AS m_trans_script,
                JSON_ARRAYAGG(
                    JSON_OBJECT(
                        'ques_id', q.id,
                        'ques_number', q.question_number,
                        'ques_content', q.content,
                        'ans_list', (
                            SELECT JSON_ARRAYAGG(
                                JSON_OBJECT(
                                    'ans_id', a.id,
                                    'is_correct', a.is_correct,
                                    'content', a.content
                                )
                            )
                            FROM toeicapp_answer a
                            WHERE a.question_id = q.id
                        )
                    )
                ) AS ques_list
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
$$ DELIMITER ;
