from pydantic import BaseModel, field_validator
from typing import List, Optional


from app.util.languge_util import LANG_MAP, LangCode


class AnsDetailResp(BaseModel):
    ans_id: int
    content: str
    is_correct: bool


class QuesDetailResp(BaseModel):
    ques_id: int
    ques_number: int
    ques_content: str
    ans_list: List[AnsDetailResp]


class MediaQuesDetailResp(BaseModel):
    media_ques_id: int
    media_ques_name: str
    media_ques_main_parag: str
    media_ques_audio_script: Optional[str] = None
    media_ques_explain: Optional[str] = None
    media_ques_trans_script: Optional[str] = None
    ques_list: List[QuesDetailResp]


class PartDetailResp(BaseModel):
    part_id: int
    part_order: str
    part_title: str
    part_audio_url: Optional[str] = None
    media_ques_list: List[MediaQuesDetailResp]


class TestDetailResp(BaseModel):
    part_list: List[PartDetailResp]


class PartSummaryResp(BaseModel):
    part_id: int
    part_order: str
    part_title: str
    total_ques: int


class TestSummaryResp(BaseModel):
    test_id: int
    test_title: str
    test_dura: int
    test_descrip: str
    part_list: List[PartSummaryResp]


class GeminiTransQuesResp(BaseModel): 
    ques_id: int
    ques_content: str
    ans_list: list[str]
    lang_id: LangCode
    
    @field_validator('lang_id')
    @classmethod
    def validate_lang_id(cls, v):
        if v not in LANG_MAP:
            raise ValueError(f'Invalid language code. Must be one of: {list(LANG_MAP.keys())}')
        return v


class GeminiTransQuesReq(BaseModel):
    ques_id: int
    lang_id: LangCode
    
    @field_validator('lang_id')
    @classmethod
    def validate_lang_id(cls, v):
        if v not in LANG_MAP:
            raise ValueError(f'Invalid language code. Must be one of: {list(LANG_MAP.keys())}')
        return v


class GeminiTransImgReq(BaseModel):
    media_id: int
    lang_id: LangCode
    
    @field_validator('lang_id')
    @classmethod
    def validate_lang_id(cls, v):
        if v not in LANG_MAP:
            raise ValueError(f'Invalid language code. Must be one of: {list(LANG_MAP.keys())}')
        return v





