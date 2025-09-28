import json
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional


from app.features.history.schemas import (
    HistoryResponse, 
    HistoryCreateRequest, 
    HistoryResultDetailResponse, 
    HitoryResultListResponse
)
from app.core.mysql_connection import get_db_cursor
from app.features.auth.dependencies import get_current_user
from app.features.history.queries import (
    INSERT_HISTORY,
    UPDATE_HISTORY_BY_USER,
    SELECT_HISTORY_BY_ID, 
    SELECT_HISTORY_BY_STATUS,
    SELECT_CALCULATE_DATAPROGRESS_RESULT_BY_HISTORY_ID,
    SELECT_CALCULATE_CORRECT_ANSWER_BY_HISTORY_ID,
    SELECT_SUBMIT_HISTORY_BY_USER,
    GET_TITLE_OF_TEST,
    SELECT_COUNT_QUESTION_BY_TEST, 
    select_count_question_by_multiple_part,
)


router = APIRouter()


@router.post("", response_model=dict)
async def create_submit_history(
    req: HistoryCreateRequest, 
    current_user: dict = Depends(get_current_user)
):
    try:
        user_id = current_user.get("user_id")
        dataprogress_json = json.dumps(req.dataprogress)
        part_json = json.dumps(req.part)

        with get_db_cursor() as cursor:
            # Check existing "save"
            cursor.execute(
                SELECT_HISTORY_BY_STATUS, 
                (user_id, req.test_id, "save")
            )
            history_id = None
            
            existing_saved = cursor.fetchone()
            if existing_saved:
                history_id = existing_saved.get("id")
                cursor.execute(
                    UPDATE_HISTORY_BY_USER,
                    (
                        dataprogress_json,
                        req.type,
                        part_json,
                        req.time,
                        req.status,
                        user_id, 
                        req.test_id,
                    ),
                )
            else:
                cursor.execute(
                    INSERT_HISTORY,
                    (
                        dataprogress_json,
                        req.type,
                        part_json,
                        req.time,
                        req.test_id,
                        user_id,
                        req.status,
                    ),
                )
                history_id = cursor.lastrowid

        # commit sẽ tự chạy khi ra khỏi with (commit_on_exit=True mặc định)
        return {"id": history_id, "message": f"History {req.type} successfully"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Error in create history controller",
                "error": str(e),
            },
        )


@router.get("/save", response_model=Optional[HistoryResponse])
async def get_save_progress_history(test_id: int, current_user: dict = Depends(get_current_user)):
    try:
        with get_db_cursor() as cursor:
            user_id = current_user.get("user_id")
            cursor.execute(SELECT_HISTORY_BY_STATUS, (user_id, test_id, 'save'))
            save_progress = cursor.fetchone()
            
            if not save_progress:
                return None

            return save_progress
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Error in get save history",
                "error": str(e),
            },
        )


@router.get("/result/list", response_model=Optional[List[HitoryResultListResponse]])
async def get_result_list(current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user.get("user_id")
        with get_db_cursor() as cursor:
            cursor.execute(SELECT_SUBMIT_HISTORY_BY_USER, (user_id,))
            submit_history_list = cursor.fetchall()
            
            
            if not submit_history_list:
                return []
            
            results = []
            for history in submit_history_list:

                # Prepare data
                history_id = history.get("id")
                part_id_list = json.loads(history.get("part"))
                test_id = history.get("test_id")
                test_type = history.get("type")
                create_at = history.get("create_at")
                duration = history.get("time")
                
                # Get test info
                cursor.execute(GET_TITLE_OF_TEST, (test_id,))
                row = cursor.fetchone()
                test_name = row.get("title")
                
                # Handle question count
                total_question = 0
                if test_type == "FullTest":
                    # FullTest: count toàn bộ câu hỏi theo test_id
                    cursor.execute(SELECT_COUNT_QUESTION_BY_TEST, (test_id,))
                    row = cursor.fetchone()
                    total_question = row.get("question_by_test_count")
                elif test_type == "Practice":
                    # PracticeTest: count theo danh sách part_orders
                    part_ids = [str(p) for p in part_id_list]
                    query = select_count_question_by_multiple_part(part_ids)
                    cursor.execute(query, (test_id, *part_ids))
                    row = cursor.fetchone()
                    total_question = row.get("question_by_multiple_part_count")
                
                # Handle calculating result
                cursor.execute(SELECT_CALCULATE_CORRECT_ANSWER_BY_HISTORY_ID, (history_id,))
                row = cursor.fetchone()
                correct_count = row.get("correct_count")
                score = f"{correct_count}/{total_question}" if total_question > 0 else "0/0"

                # Append result for this history
                results.append({
                    "history_id": history_id,
                    "test_id": test_id,
                    "test_type": test_type,
                    "create_at": create_at,
                    "duration": duration,
                    "test_name": test_name,
                    "score": score,
                    "part_list": part_id_list
                })

        return results
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Error in get result list controller",
                "error": str(e),
            },
        )


@router.get("/result/detail", response_model=HistoryResultDetailResponse)
async def get_result_detail(history_id: int, _: dict = Depends(get_current_user)):
    try:
        with get_db_cursor() as cursor:
            cursor.execute(SELECT_HISTORY_BY_ID, (history_id,))
            history = cursor.fetchone()
            if not history: 
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User history not found"
                )
            
            # Prepare data
            history_id = history.get("id")
            part_id_list = json.loads(history.get("part"))
            test_id = history.get("test_id")
            test_type = history.get("type")
            create_at = history.get("create_at")
            duration = history.get("time")
            dataprogress = history.get("dataprogress")
            
            cursor.execute(GET_TITLE_OF_TEST, (test_id,))
            row = cursor.fetchone()
            test_name = row.get("title")
            
            # Handle question count
            total_question = 0
            # FullTest: count toàn bộ câu hỏi theo test_id
            if test_type == "FullTest":
                cursor.execute(SELECT_COUNT_QUESTION_BY_TEST, (test_id,))
                row = cursor.fetchone()
                total_question = row.get("question_by_test_count")
            # # PracticeTest: count theo danh sách part_orders
            elif test_type == "Practice":
                # PracticeTest: count theo danh sách part_orders
                part_ids = [str(p) for p in part_id_list]
                query = select_count_question_by_multiple_part(part_ids)
                cursor.execute(query, (test_id, *part_ids))
                row = cursor.fetchone()
                total_question = row.get("question_by_multiple_part_count")

            # Handle calculating result
            cursor.execute(SELECT_CALCULATE_DATAPROGRESS_RESULT_BY_HISTORY_ID, (history_id,))
            row = cursor.fetchone()
            correct_count = row.get("correct_count")
            incorrect_count = row.get("incorrect_count")
            correct_listening = row.get("correct_listening")
            correct_reading = row.get("correct_reading")
            
            total_answer = incorrect_count + correct_count
            no_answer = total_question - total_answer
            accuracy = (correct_count / total_answer) * 100 if total_answer > 0 else 0
        
        return {
            "history_id": history_id,
            "test_id": test_id,
            "test_type": test_type, 
            "test_name": test_name,
            "correct_count": correct_count, 
            "incorrect_count": incorrect_count,
            "correct_listening": correct_listening,
            "correct_reading": correct_reading,
            "no_answer": no_answer,
            "total_question": total_question,
            "accuracy": round(accuracy, 2),
            "create_at": create_at,
            "duration": duration,
            "dataprogress": dataprogress,
            "part_list": part_id_list
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Error in get result detail controller",
                "error": {e}
            }
        )
