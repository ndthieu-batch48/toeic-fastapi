DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `SELECT_TEST_DETAIL_PROC`(
    IN pTEST_ID INT,
    OUT pJSON_RESULT JSON
)
BEGIN
    SELECT JSON_OBJECT(
        'part_list', JSON_ARRAYAGG(
            JSON_OBJECT(
                'part_id', part_id,
                'part_order', part_order,
                'part_title', part_title,
                'part_audio_url', part_audio_url,
                'media_list', media_list
            )
        )
    ) INTO pJSON_RESULT
    FROM (
        SELECT 
            tmp.part_id,
            tmp.part_order,
            tmp.part_title,
            tmp.part_audio_url,
            JSON_ARRAYAGG(
                JSON_OBJECT(
                    'media_id', media_id,
                    'media_name', media_name,
                    'media_paragraph_main', paragrap_main,
                    'media_audio_script', media_audio_script,
                    'media_explain_question', media_explain_question,
                    'media_translate_script', media_translate_script,
                    'question_list', question_list
                )
            ) AS media_list
        FROM (
            SELECT 
                p.id AS part_id,
                p.part_order,
                p.title AS part_title,
                p.audio_url AS part_audio_url,
                m.id AS media_id,
                m.media_name,
                m.paragrap_main,
                m.audio_script AS media_audio_script,
                m.explain_question AS media_explain_question,
                m.translate_script AS media_translate_script,
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
        GROUP BY tmp.part_id, tmp.part_order, tmp.part_title, tmp.part_audio_url
    ) final;
END$$
DELIMITER ;