from pydantic import BaseModel, field_validator
from typing import List, Optional


from app.util.languge_util import LANGUAGE_MAP, LanguageCode


class AnsDetailRes(BaseModel):
    ans_id: int
    content: str
    is_correct: bool

class QuesDetailRes(BaseModel):
    ques_id: int
    ques_number: int
    ques_content: str
    ans_list: List[AnsDetailRes]

class MediaQuesDetailRes(BaseModel):
    media_ques_id: int
    media_ques_name: str
    media_ques_main_para: str
    media_ques_audio_script: Optional[str] = None
    media_ques_explain: Optional[str] = None
    media_ques_trans_script: Optional[str] = None
    ques_list: List[QuesDetailRes]

class PartDetailRes(BaseModel):
    part_id: int
    part_order: str
    part_title: str
    part_audio_url: Optional[str] = None
    media_ques_list: List[MediaQuesDetailRes]

class TestDetailRes(BaseModel):
    part_list: List[PartDetailRes]


class PartSummaryRes(BaseModel):
    part_id: int
    part_order: str
    part_title: str
    total_ques: int


class TestSummaryRes(BaseModel):
    test_id: int
    part_list: List[PartSummaryRes]
    test_title: str
    test_duration: int
    test_description: str


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





