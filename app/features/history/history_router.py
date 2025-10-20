import json
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional


from app.features.history.history_schemas import (
    HistoryCreateResp,
    HistoryResp, 
    HistoryCreateReq, 
    HistoryResultDetailResp, 
    HitoryResultListResp
)
from app.core.mysql_connection import get_db_cursor
from app.features.auth.auth_dependencies import get_current_user
from app.features.history.history_query import (
    INSERT_HISTORY,
    UPDATE_HISTORY_BY_USER,
    SELECT_HISTORY_BY_ID, 
    SELECT_HISTORY_BY_STATUS,
    SELECT_CALCULATE_DATAPROG_RESULT_BY_HISTORY_ID,
    SELECT_CALCULATE_CORRECT_ANS_BY_HISTORY_ID,
    SELECT_SUBMIT_HISTORY_BY_USER,
    GET_TITLE_OF_TEST,
    SELECT_COUNT_QUES_BY_TEST, 
    select_count_ques_by_multiple_part,
    select_multiple_part_order_by_part_id
)


router = APIRouter()


@router.post("", response_model=HistoryCreateResp)
async def create_submit_history(
    req: HistoryCreateReq, 
    current_user: dict = Depends(get_current_user)
):
    try:
        user_id = current_user.get("user_id")
        dataprogress_json = json.dumps(req.dataprog)
        part_json = json.dumps(req.part_id_list)

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
                        req.dura,
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
                        req.dura,
                        req.test_id,
                        user_id,
                        req.status,
                    ),
                )
                history_id = cursor.lastrowid

        # commit sẽ tự chạy khi ra khỏi with (commit_on_exit=True mặc định)
        return {
            "history_id": history_id,
            "status": req.status,
            "message": f"History {req.type} successfully",
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Error in create history controller",
                "error": str(e),
            },
        )


@router.get("/save", response_model=Optional[HistoryResp])
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


@router.get("/result/list", response_model=Optional[List[HitoryResultListResp]])
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
                dura = history.get("dura")
                
                # Get test info
                cursor.execute(GET_TITLE_OF_TEST, (test_id,))
                row = cursor.fetchone()
                test_name = row.get("title")
                
                # Get part info. If user select Full Test, return all parts 
                if part_id_list:
                    part_order_query = select_multiple_part_order_by_part_id(part_id_list)
                    cursor.execute(part_order_query, (*part_id_list,))
                    part_order_rows = cursor.fetchall()
                    part_order_list = [row.get("part_order") for row in part_order_rows]
                else:
                    part_order_list = ["Part 1", "Part 2", "Part 3", "Part 4", "Part 5", "Part 6", "Part 7"]
                
                # Handle question count
                total_ques = 0
                # Full Test: Counting all question by test_id
                if test_type == "FullTest":
                    cursor.execute(SELECT_COUNT_QUES_BY_TEST, (test_id,))
                    row = cursor.fetchone()
                    total_ques = row.get("ques_by_test_count")
                elif test_type == "Practice":
                # Practice Test: Counting all question by part_id_list
                    ques_count_query = select_count_ques_by_multiple_part(part_id_list)
                    cursor.execute(ques_count_query, (test_id, *part_id_list))
                    row = cursor.fetchone()
                    total_ques = row.get("ques_by_multiple_part_count")
                
                # Handle calculating result
                cursor.execute(SELECT_CALCULATE_CORRECT_ANS_BY_HISTORY_ID, (history_id,))
                row = cursor.fetchone()
                correct_count = row.get("correct_count")
                score = f"{correct_count}/{total_ques}" if total_ques > 0 else "0/0"

                results.append({
                    "history_id": history_id,
                    "test_id": test_id,
                    "test_type": test_type,
                    "create_at": create_at,
                    "dura": dura,
                    "test_name": test_name,
                    "score": score,
                    "part_id_list": part_id_list,
                    "part_order_list": part_order_list
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


@router.get("/result/detail", response_model=HistoryResultDetailResp)
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
            dura = history.get("dura")
            dataprog = history.get("dataprog")
            
            cursor.execute(GET_TITLE_OF_TEST, (test_id,))
            row = cursor.fetchone()
            test_name = row.get("title")
            
            # Handle question count
            total_ques = 0
            # Full Test: Counting all question by test_id
            if test_type == "FullTest":
                cursor.execute(SELECT_COUNT_QUES_BY_TEST, (test_id,))
                row = cursor.fetchone()
                total_ques = row.get("ques_by_test_count")
            # # Practice Test: count theo danh sách part_orders
            elif test_type == "Practice":
                # PracticeTest: Counting all question by part_id_list
                ques_count_query = select_count_ques_by_multiple_part(part_id_list)
                cursor.execute(ques_count_query, (test_id, *part_id_list))
                row = cursor.fetchone()
                total_ques = row.get("ques_by_multiple_part_count")

            # Handle calculating result
            cursor.execute(SELECT_CALCULATE_DATAPROG_RESULT_BY_HISTORY_ID, (history_id,))
            row = cursor.fetchone()
            correct_count = row.get("correct_count")
            incorrect_count = row.get("incorrect_count")
            correct_listening = row.get("correct_listening")
            correct_reading = row.get("correct_reading")
            
            total_ans = incorrect_count + correct_count
            no_ans = total_ques - total_ans
            accuracy = (correct_count / total_ques) * 100 if total_ans > 0 else 0
        
        return {
            "history_id": history_id,
            "test_id": test_id,
            "test_type": test_type, 
            "test_name": test_name,
            "correct_count": correct_count, 
            "incorrect_count": incorrect_count,
            "correct_listening": correct_listening,
            "correct_reading": correct_reading,
            "no_ans": no_ans,
            "total_ques": total_ques,
            "accuracy": round(accuracy, 2),
            "create_at": create_at,
            "dura": dura,
            "dataprog": dataprog,
            "part_id_list": part_id_list,
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
