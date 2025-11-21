import json
import os
from typing import List
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from app.core.gemini_client import generate_text_with_gemini
from app.core.mysql_connection import get_db_cursor
from app.feature.test.test_query import (
    SELECT_AUDIO_SCRIPT_BY_MEDIA_ID,
    SELECT_BASE64_IMAGE_BY_MEDIA_ID,
    SELECT_QUESTION_BLOCK_JSON_BY_ID,
    SELECT_PART_AUDIO_URL,
    SELECT_QUESTION_EXPLAIN_BLOCK_JSON_BY_ID,
    SELECT_QUESTION_TRANSLATE_JSON,
    SELECT_QUESTION_EXPLAIN_JSON,
    UPDATE_QUESTION_TRANSLATE_JSON_SCRIPT,
    UPDATE_QUESTION_EXPLAIN_JSON_SCRIPT,
)
from app.feature.test.test_schema import (
    GeminiExplainQuestionRequest,
    GeminiExplainQuestionResponse,
    GeminiTranslateAudioScriptRequest,
    GeminiTranslateImageRequest, 
    GeminiTranslateQuestionRequest, 
    GeminiTranslateQuestionResponse,
    TestDetailResponse,
    TestSummaryResponse)
from app.feature.test.test_prompt_helper import  (
    build_question_explain_prompt, 
    build_question_translation_prompt, 
    clean_gemini_response
)
from app.feature.test.test_audio_util import resolve_audio_file_path


router = APIRouter()


@router.get("", response_model=List[TestSummaryResponse], description="Get all test summaries")
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


@router.get("/{id}" , response_model=TestDetailResponse, description="Returns detailed information for a TOEIC test")
async def get_test_detail(id: int):
    try:        
        with get_db_cursor(dictionary=False) as cursor:
            result_args = cursor.callproc("SELECT_TEST_DETAIL_PROC", [id, 0])
            
            test_json = json.loads(result_args[1])
            
            if not test_json:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail=f"Test detail not found for id {id}"
                )
                
            return test_json
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Error in get test detail controller",
                "error": str(e),
            },
        )


@router.get("/{test_id}/part/{part_id}/audio/url")
async def get_audio_url(test_id: int, part_id: int):
    """Get the stream URL for audio. Returns null for Parts 5, 6, 7."""
    try:
        with get_db_cursor() as cursor:
            cursor.execute(SELECT_PART_AUDIO_URL, (test_id, part_id))
            row = cursor.fetchone()
            
            if not row or not row.get('audio_url'):
                return {"audio_stream_url": None}
            
            # Return the stream URL that points to the stream endpoint
            stream_url = f"tests/{test_id}/part/{part_id}/audio/stream"
            return {"audio_stream_url": stream_url}
    except HTTPException:
        raise        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in get audio URL controller: {str(e)}"
        )


@router.get("/{test_id}/part/{part_id}/audio/stream")
async def stream_part_audio(test_id: int, part_id: int):
    try:
        with get_db_cursor() as cursor:
            cursor.execute(SELECT_PART_AUDIO_URL, (test_id, part_id))
            row = cursor.fetchone()
            
            if not row or not row.get('audio_url'):
                return None
            
            part_audio_url = row['audio_url']
            audio_file_path = resolve_audio_file_path(part_audio_url)
            
            if not audio_file_path or not os.path.exists(audio_file_path):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Audio file not found: {part_audio_url}"
                )
            
            return FileResponse(
                path=audio_file_path,
                media_type="audio/mpeg",
                filename=os.path.basename(audio_file_path),
                headers={
                    "Accept-Ranges": "bytes",
                    "Cache-Control": "public, max-age=3600"
                }
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in get part audio controller: {str(e)}"
        )


@router.post(
    "/gemini/translate/question",
    response_model=GeminiTranslateQuestionResponse,
    description="Translate a TOEIC question to the target language using Gemini AI."
)
async def translate_question(request: GeminiTranslateQuestionRequest):
    try:
        with get_db_cursor() as cursor:
            # Check if translation already exists in database
            cursor.execute(SELECT_QUESTION_TRANSLATE_JSON, (request.question_id,))
            cached_row = cursor.fetchone()
            
            if cached_row and cached_row.get('question_translate_json'):
                cached_data = cached_row['question_translate_json']
                # Parse if it's a string, otherwise use as-is
                if isinstance(cached_data, str):
                    cached_data = json.loads(cached_data)
                # Check if the cached data matches the requested language
                if cached_data.get('language_id') == request.language_id:
                    return cached_data
            
            # If no cached data, proceed with translation
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
            
            # Clean the response: remove markdown code blocks if present
            cleaned_response = clean_gemini_response(gemini_response)
            
            response = json.loads(cleaned_response)
            
            # Update the translation in the database
            cursor.execute(
                UPDATE_QUESTION_TRANSLATE_JSON_SCRIPT,
                (json.dumps(response), request.question_id)
            )

        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in translate question controller: {str(e)}"
        )


@router.post(
    "/gemini/explain/question",
    response_model=GeminiExplainQuestionResponse,
    description="Explain a TOEIC question to the target language using Gemini AI."
)
async def explain_question(request: GeminiExplainQuestionRequest):
    try:
        with get_db_cursor() as cursor:
            # Check if explanation already exists in database
            cursor.execute(SELECT_QUESTION_EXPLAIN_JSON, (request.question_id,))
            cached_row = cursor.fetchone()
            
            if cached_row and cached_row.get('question_explain_json'):
                cached_data = cached_row['question_explain_json']
                # Parse if it's a string, otherwise use as-is
                if isinstance(cached_data, str):
                    cached_data = json.loads(cached_data)
                # Check if the cached data matches the requested language
                if cached_data.get('language_id') == request.language_id:
                    return cached_data
            
            # If no cached data, proceed with explanation generation
            cursor.execute(SELECT_QUESTION_EXPLAIN_BLOCK_JSON_BY_ID, (request.question_id,))
            row = cursor.fetchone()
            if not row or not row.get('question_explain_block_json'):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Question not found"
                )
            question_explain_block_json = row['question_explain_block_json']

            prompt = build_question_explain_prompt(question_explain_block_json, request.language_id)
            gemini_response = generate_text_with_gemini(prompt)
            if not gemini_response:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to get explanation from Gemini"
                )
            
            # Clean the response: remove markdown code blocks if present
            cleaned_response = clean_gemini_response(gemini_response)
            
            response = json.loads(cleaned_response)
            
            # Update the explanation in the database
            cursor.execute(
                UPDATE_QUESTION_EXPLAIN_JSON_SCRIPT,
                (json.dumps(response), request.question_id)
            )

        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in translate question controller: {str(e)}"
        )

@router.post("/gemini/translate/image", response_model=dict)
async def translate_image(request: GeminiTranslateImageRequest):
    try:
        with get_db_cursor() as cursor:
            cursor.execute(SELECT_BASE64_IMAGE_BY_MEDIA_ID, (request.media_id,))
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
            detail=f"Error in translate image controller: {str(e)}"
        )


@router.post("/gemini/translate/audio-script", response_model=dict)
async def translate_audio_script(request: GeminiTranslateAudioScriptRequest):
    try:
        with get_db_cursor() as cursor:
            cursor.execute(SELECT_AUDIO_SCRIPT_BY_MEDIA_ID, (request.media_id,))
            row = cursor.fetchone()
            if not row or not row.get('audio_script'):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Audio script not found"
                )
            script = row['audio_script']

            return  {"script": script}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in translate audio script controller: {str(e)}"
        )