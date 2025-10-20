import json
import os
from typing import List
from fastapi import APIRouter, HTTPException, status, Query
from fastapi.responses import FileResponse

from app.core.gemini_client import generate_text_with_gemini
from app.core.mysql_connection import get_db_cursor
from app.features.test.test_query import SELECT_QUES_BLOCK_JSON_BY_ID, SELECT_PART_AUDIO_URL
from app.features.test.test_schemas import (
    GeminiTransImgReq, 
    GeminiTransQuesReq, 
    GeminiTransQuesResp,
    TestDetailResp,
    TestSummaryResp)
from app.features.test.test_prompt_helper import build_ques_trans_prompt
from app.util.audio_util import resolve_audio_file_path


router = APIRouter()


@router.get("", response_model=List[TestSummaryResp], description="Get all test summaries")
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


@router.get("/{id}" , response_model=TestDetailResp, description="Returns detailed information for a specific TOEIC test, including selected parts and questions")
async def get_test_detail(
    id: int,
    part_ids: List[int] = Query(
        default=[],
        description="List of part IDs to filter by",
        example=[1, 2, 3]
    )
):
    try:        
        # Convert list of integers to comma-separated string for the stored procedure
        part_id_str = ",".join(map(str, part_ids)) if part_ids and len(part_ids) > 0 else None
        
        with get_db_cursor(dictionary=False) as cursor:
            result_args = cursor.callproc("SELECT_TEST_DETAIL_PROC", [id, part_id_str, 0])
            
            test_json = json.loads(result_args[2])
            
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


@router.post(
    "/gemini/trans/ques",
    response_model=GeminiTransQuesResp,
    description="Translate a TOEIC question to the target language using Gemini AI."
)
async def trans_ques(req: GeminiTransQuesReq):
    try:
        with get_db_cursor() as cursor:
            cursor.execute(SELECT_QUES_BLOCK_JSON_BY_ID, (req.ques_id,))
            row = cursor.fetchone()
            if not row or not row.get('ques_block_json'):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Question not found"
                )
            ques_block_json = row['ques_block_json']

            prompt = build_ques_trans_prompt(ques_block_json, req.lang_id)
            gemini_resp = generate_text_with_gemini(prompt)
            if not gemini_resp:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to get translation from Gemini"
                )
            
            resp = json.loads(gemini_resp)            

        return resp
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in translate question controller: {str(e)}"
        )


SELECT_BASE64_IMAGE_BY_ID = """
select * from toeicapp_media where id = %s
"""
@router.post("/gemini/translate/image", response_model=dict)
async def translate_image(request: GeminiTransImgReq):
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