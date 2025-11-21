from typing import Dict
from pydantic import BaseModel, field_validator
from typing import List, Optional


from app.util.languge_util import LANGUAGE_MAP, LanguageCode


class AnswerDetailResponse(BaseModel):
    answer_id: int
    content: str
    is_correct: bool


class QuestionDetailResponse(BaseModel):
    question_id: int
    question_number: int
    question_content: str
    answer_list: List[AnswerDetailResponse]


class MediaQuestionDetailResponse(BaseModel):
    media_question_id: int
    media_question_name: str
    media_question_main_paragraph: str
    media_question_audio_script: Optional[str] = None
    question_list: List[QuestionDetailResponse]


class PartDetailResponse(BaseModel):
    part_id: int
    part_order: str
    part_title: str
    part_audio_url: Optional[str] = None
    media_question_list: List[MediaQuestionDetailResponse]


class TestDetailResponse(BaseModel):
    part_list: List[PartDetailResponse]


class PartSummaryResponse(BaseModel):
    part_id: int
    part_order: str
    part_title: str
    total_question: int


class TestSummaryResponse(BaseModel):
    test_id: int
    test_title: str
    test_duration: int
    test_description: str
    part_list: List[PartSummaryResponse]


class GeminiTranslateQuestionResponse(BaseModel): 
    question_id: int
    question_content: str
    answer_list: list[str]
    language_id: LanguageCode
    
    @field_validator('language_id')
    @classmethod
    def validate_lang_id(cls, v):
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


class GeminiTranslateAudioScriptRequest(BaseModel):
    media_id: int
    language_id: LanguageCode
    
    @field_validator('language_id')
    @classmethod
    def validate_lang_id(cls, v):
        if v not in LANGUAGE_MAP:
            raise ValueError(f'Invalid language code. Must be one of: {list(LANGUAGE_MAP.keys())}')
        return v


class GeminiExplainQuestionRequest(BaseModel):
    question_id: int
    language_id: LanguageCode
    
    @field_validator('language_id')
    @classmethod
    def validate_lang_id(cls, v):
        if v not in LANGUAGE_MAP:
            raise ValueError(f'Invalid language code. Must be one of: {list(LANGUAGE_MAP.keys())}')
        return v


class GeminiExplainQuestionResponse(BaseModel):
    question_id: int
    question_ask: str
    question_need: str
    correct_answer_reason: str
    incorrect_answer_reason: Dict[str, str]
    language_id: str
    
    @field_validator('language_id')
    @classmethod
    def validate_language_id(cls, v):
        if v not in LANGUAGE_MAP:
            raise ValueError(f'Invalid language code. Must be one of: {list(LANGUAGE_MAP.keys())}')
        return v



