import json
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional


from app.feature.history.history_schema import (
    HistoryCreateResponse,
    HistoryResponse, 
    HistoryCreateRequest, 
    HistoryResultDetailResponse, 
    HistoryResultListResponse
)
from app.core.mysql_connection import get_db_cursor
from app.feature.auth.auth_dependencies import get_current_user
from app.feature.history.history_query import (
    INSERT_HISTORY,
    UPDATE_HISTORY_BY_USER,
    SELECT_HISTORY_BY_ID, 
    SELECT_HISTORY_BY_STATUS,
    SELECT_CALCULATE_CORRECT_INCORRECT_FOR_TEST_BY_HISTORY_ID,
    SELECT_CALCULATE_CORRECT_ANSWER_BY_HISTORY_ID,
    SELECT_CALCULATE_CORRECT_INCORRECT_FOR_EACH_PART_BY_HISTORY_ID,
    SELECT_SUBMIT_HISTORY_BY_USER,
    GET_TITLE_OF_TEST,
    SELECT_COUNT_QUESTIONS_BY_TEST, 
    select_count_questions_by_multiple_part,
    select_multiple_part_order_by_part_id
)
from app.feature.test.test_const import TEST_TYPE


router = APIRouter()


@router.post("", response_model=HistoryCreateResponse)
async def create_submit_history(
    request: HistoryCreateRequest, 
    current_user: dict = Depends(get_current_user)
):
    try:
        user_id = current_user.get("user_id")
        data_progress_json = json.dumps(request.data_progress)
        part_json = json.dumps(request.part_id_list)
        
        # Ensure fallback values of 0 for durations
        practice_duration = request.practice_duration if request.practice_duration is not None else 0
        exam_duration = request.exam_duration if request.exam_duration is not None else 0

        with get_db_cursor() as cursor:
            # Check existing "save"
            cursor.execute(
                SELECT_HISTORY_BY_STATUS, 
                (user_id, request.test_id, "save")
            )
            history_id = None
            
            existing_saved = cursor.fetchone()
            if existing_saved:
                history_id = existing_saved.get("id")
                cursor.execute(
                    UPDATE_HISTORY_BY_USER,
                    (
                        data_progress_json,
                        request.type,
                        part_json,
                        practice_duration,
                        exam_duration,
                        request.status,
                        user_id, 
                        request.test_id,
                    ),
                )
            else:
                cursor.execute(
                    INSERT_HISTORY,
                    (
                        data_progress_json,
                        request.type,
                        part_json,
                        practice_duration,
                        exam_duration,
                        request.test_id,
                        user_id,
                        request.status,
                    ),
                )
                history_id = cursor.lastrowid

        # commit sẽ tự chạy khi ra khỏi with (commit_on_exit=True mặc định)
        return {
            "history_id": history_id,
            "status": request.status,
            "message": f"History {request.type} successfully",
        }

    except HTTPException:
        raise
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
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Error in get save history",
                "error": str(e),
            },
        )


@router.get("/result/list", response_model=Optional[List[HistoryResultListResponse]])
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
                part_id_list = json.loads(history.get("part_id_list"))
                test_id = history.get("test_id")
                test_type = history.get("type")
                create_at = history.get("create_at")
                practice_duration = history.get("practice_duration") or 0
                exam_duration = history.get("exam_duration") or 0

                # Get test info
                cursor.execute(GET_TITLE_OF_TEST, (test_id,))
                row = cursor.fetchone()
                test_name = row.get("title")

                # Get part info. 
                # If user selected PRACTICE MODE, get part orders by part_id_list
                if part_id_list:
                    part_order_query = select_multiple_part_order_by_part_id(part_id_list)
                    cursor.execute(part_order_query, (*part_id_list,))
                    part_order_rows = cursor.fetchall()
                    part_order_list = [row.get("part_order") for row in part_order_rows]
                
                # If user selected EXAM MODE, return all parts
                else:
                    part_order_list = ["Part 1", "Part 2", "Part 3", "Part 4", "Part 5", "Part 6", "Part 7"]

                # Handle question count
                total_question = 0
                # EXAM MODE: Counting all question by test_id
                if test_type == TEST_TYPE.EXAM:
                    cursor.execute(SELECT_COUNT_QUESTIONS_BY_TEST, (test_id,))
                    row = cursor.fetchone()
                    total_question = row.get("question_by_test_count")

                # PRACTICE MODE: Counting all question by part_orders
                elif test_type == TEST_TYPE.PRACTICE:
                    question_count_query = select_count_questions_by_multiple_part(part_id_list)
                    cursor.execute(question_count_query, (test_id, *part_id_list))
                    row = cursor.fetchone()
                    total_question = row.get("question_by_multiple_part_count")

                # Handle calculating result
                cursor.execute(SELECT_CALCULATE_CORRECT_ANSWER_BY_HISTORY_ID, (history_id,))
                row = cursor.fetchone()
                correct_count = row.get("correct_count")
                score = f"{correct_count}/{total_question}" if total_question > 0 else "0/0"

                results.append({
                    "history_id": history_id,
                    "test_id": test_id,
                    "test_type": test_type,
                    "create_at": create_at,
                    "practice_duration": practice_duration,
                    "exam_duration": exam_duration,
                    "test_name": test_name,
                    "score": score,
                    "part_id_list": part_id_list,
                    "part_order_list": part_order_list
                })

        return results
    except HTTPException:
        raise
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
            part_id_list = json.loads(history.get("part_id_list"))
            test_id = history.get("test_id")
            test_type = history.get("type")
            create_at = history.get("create_at")
            practice_duration = history.get("practice_duration") or 0
            exam_duration = history.get("exam_duration") or 0
            data_progress = history.get("data_progress")
            
            cursor.execute(GET_TITLE_OF_TEST, (test_id,))
            row = cursor.fetchone()
            test_name = row.get("title")
            
            # Handle question count
            total_question = 0
            # EXAM MODE: Counting all question by test_id
            if test_type == TEST_TYPE.EXAM:
                cursor.execute(SELECT_COUNT_QUESTIONS_BY_TEST, (test_id,))
                row = cursor.fetchone()
                total_question = row.get("question_by_test_count")
            
            # PRACTICE MODE: Counting all question by part_orders
            elif test_type == TEST_TYPE.PRACTICE:
                question_count_query = select_count_questions_by_multiple_part(part_id_list)
                cursor.execute(question_count_query, (test_id, *part_id_list))
                row = cursor.fetchone()
                total_question = row.get("question_by_multiple_part_count")

            # Handle calculating result
            cursor.execute(SELECT_CALCULATE_CORRECT_INCORRECT_FOR_TEST_BY_HISTORY_ID, (history_id,))
            row = cursor.fetchone()
            correct_count = row.get("correct_count")
            incorrect_count = row.get("incorrect_count")
            correct_listening = row.get("correct_listening")
            correct_reading = row.get("correct_reading")
            
            total_answer = incorrect_count + correct_count
            no_answer = total_question - total_answer
            accuracy = (correct_count / total_question) * 100 if total_answer > 0 else 0
            
            # Calculate correct answer by part
            cursor.execute(SELECT_CALCULATE_CORRECT_INCORRECT_FOR_EACH_PART_BY_HISTORY_ID, (history_id,))
            part_results = cursor.fetchall()
            result_by_part = [
                {
                    "part_order": row.get("part_order"),
                    "total_question": row.get("total_question"),
                    "correct_count": row.get("correct_count"),
                    "incorrect_count": row.get("incorrect_count"),
                    "no_answer": row.get("total_question") - (row.get("correct_count") + row.get("incorrect_count")),
                }
                for row in part_results
            ]
        
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
            "practice_duration": practice_duration,
            "exam_duration": exam_duration,
            "data_progress": data_progress,
            "part_id_list": part_id_list,
            "result_by_part": result_by_part,
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
