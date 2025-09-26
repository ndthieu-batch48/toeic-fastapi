import json
from fastapi import APIRouter, HTTPException, status


from app.core.gemini_client import generate_text_with_gemini
from app.core.mysql_connection import get_db_cursor
from app.features.test.queries import SELECT_QUESTION_BLOCK_JSON_BY_ID
from app.features.test.schemas import (
    GeminiTranslateImageRequest, 
    GeminiTranslateQuestionRequest, 
    GeminiTranslateQuestionResponse)
from app.features.test.prompt_helper import build_question_translation_prompt


router = APIRouter()


@router.get("/all")
async def get_all_test():
    try:
        with get_db_cursor(dictionary=False) as cursor:
            result_args = cursor.callproc("SELECT_ALL_TEST_PROC", [0])

            test_json = json.loads(result_args[0])
            
            if not test_json:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail="List tests not found"
                )
            
            return test_json
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Error in get all test controller",
                "error": str(e),
            },
        )


@router.get("/{id}")
async def get_test_detail(id: int):
    with get_db_cursor(dictionary=False) as cursor:
        result_args = cursor.callproc("SELECT_TEST_DETAIL_PROC", [id, 0])
        
        test_json = json.loads(result_args[1]) 
        
        return test_json


@router.get("/{id}/parts/{part_id}/detail")
async def get_part_detail(id: int, part_id: int):
    try:
        with get_db_cursor(dictionary=False) as cursor:
            result_args = cursor.callproc("SELECT_PART_DETAIL_PROC", [id, part_id, 0])
            
            part_json = json.loads(result_args[2])
            
            if  part_json is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail=f"Part detail not found for test_id {id} and part_id {part_id}"
                )
            
            return part_json
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Error in get part detail controller",
                "error": {e}
            }
        )


@router.post("/gemini/translate/question", response_model=GeminiTranslateQuestionResponse)
async def translate_question(request: GeminiTranslateQuestionRequest):
    try:
        with get_db_cursor() as cursor:
            cursor.execute(SELECT_QUESTION_BLOCK_JSON_BY_ID, (request.question_id,))
            row = cursor.fetchone()
            if not row or not row.get('question_block_json'):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Question not found"
                )
            question_block_json = row['question_block_json']

            prompt = build_question_translation_prompt(question_block_json, request.language_id)
            gemini_response = generate_text_with_gemini(prompt)
            if not gemini_response:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to get translation from Gemini"
                )
            
            response = json.loads(gemini_response)            

        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in translate question controller: {str(e)}"
        )


SELECT_BASE64_IMAGE_BY_ID = """
select * from toeicapp_media where id = %s
"""
@router.post("/gemini/translate/image", response_model=dict)
async def translate_image(request: GeminiTranslateImageRequest):
    try:
        with get_db_cursor() as cursor:
            cursor.execute(SELECT_BASE64_IMAGE_BY_ID, (request.media_id,))
            row = cursor.fetchone()
            if not row or not row.get('paragrap_main'):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Image not found"
                )
            img = row['paragrap_main']

            return  {"img": img}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in translate question controller: {str(e)}"
        )