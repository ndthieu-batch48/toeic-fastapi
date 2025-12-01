from datetime import datetime
from typing import Dict, List, Literal
from pydantic import BaseModel, Json

from app.feature.test.test_const import TEST_TYPE


class HistoryResponse(BaseModel):
    id: int
    data_progress: Json[Dict[str, str]]
    type: TEST_TYPE
    part_id_list: Json[List[str]]              
    practice_duration: int
    exam_duration: int
    test_id: int                        
    user_id: int                      
    create_at: datetime 
    status: Literal["save", "submit"]


class HistoryCreateRequest(BaseModel):
    data_progress: Dict[str, str]
    type: TEST_TYPE
    part_id_list: List[str]
    practice_duration: int | None = None
    exam_duration: int | None = None
    test_id: int
    status: Literal["save", "submit"]


class HistoryCreateResponse(BaseModel):
    history_id: int
    status: str
    message: str


class PartResultDetail(BaseModel):
    part_order: str
    total_question: int
    correct_count: int
    incorrect_count: int
    no_answer: int


class HistoryResultDetailResponse(BaseModel):
    history_id: int
    test_id: int
    test_type: TEST_TYPE
    test_name: str
    correct_count: int
    incorrect_count: int
    correct_listening: int
    correct_reading: int
    no_answer: int
    total_question: int
    accuracy: float
    practice_duration: int
    exam_duration: int
    create_at: datetime
    data_progress: Json[Dict[str, str]]
    part_id_list: List[str]
    result_by_part: List[PartResultDetail]


class HistoryResultListResponse(BaseModel):
    history_id: int
    score: str
    test_id: int 
    test_type: TEST_TYPE
    test_name: str
    practice_duration: int
    exam_duration: int
    part_id_list: List[str]
    part_order_list: List[str]
    create_at: datetime