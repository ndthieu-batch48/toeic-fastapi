from pydantic import BaseModel, field_validator
from typing import List, Optional


from app.util.languge_util import LANGUAGE_MAP, LanguageCode


class AnswerDetail(BaseModel):
    answer_id: int
    content: str
    is_correct: bool

class QuestionDetail(BaseModel):
    question_id: int
    question_number: int
    question_content: str
    answer_list: List[AnswerDetail]

class MediaDetail(BaseModel):
    media_id: int
    media_name: str
    media_paragraph_main: str
    media_audio_script: Optional[str] = None
    media_explain_question: Optional[str] = None
    media_translate_script: Optional[str] = None
    question_list: List[QuestionDetail]

class PartDetail(BaseModel):
    part_id: int
    part_order: str
    part_title: str
    part_audio_url: Optional[str] = None
    media_list: List[MediaDetail]

class TestDetail(BaseModel):
    part_list: List[PartDetail]


class GeminiTranslateQuestionResponse(BaseModel): 
    question_id: int
    question_content: str
    answer_list: list[str]
    language_id: LanguageCode
    
    @field_validator('language_id')
    @classmethod
    def validate_language_id(cls, v):
        if v not in LANGUAGE_MAP:
            raise ValueError(f'Invalid language code. Must be one of: {list(LANGUAGE_MAP.keys())}')
        return v


class GeminiTranslateQuestionRequest(BaseModel):
    question_id: int
    language_id: LanguageCode
    
    @field_validator('language_id')
    @classmethod
    def validate_language_id(cls, v):
        if v not in LANGUAGE_MAP:
            raise ValueError(f'Invalid language code. Must be one of: {list(LANGUAGE_MAP.keys())}')
        return v


class GeminiTranslateImageRequest(BaseModel):
    media_id: int
    language_id: LanguageCode
    
    @field_validator('language_id')
    @classmethod
    def validate_language_id(cls, v):
        if v not in LANGUAGE_MAP:
            raise ValueError(f'Invalid language code. Must be one of: {list(LANGUAGE_MAP.keys())}')
        return v





