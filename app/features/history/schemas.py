from datetime import datetime
from typing import Dict, List, Literal, Optional
from pydantic import BaseModel, Json


class HistoryResponse(BaseModel):
    id: int
    dataprogress: Json[Dict[str, str]]  # JSON field
    type: str                           # varchar(20) - "Practice", "FullTest", etc.
    part: Json[List[str]]               # JSON field - ["Part 5"]
    time: int                           # int field
    test_id: int                        # bigint field
    user_id: int                        # bigint field  
    create_at: datetime                 # datetime field (note: create_at, not created_at)
    status: str                         # varchar(10) - "submit", etc.
    time_left: Optional[int] = None     # int field, can be NULL


class HistoryCreateRequest(BaseModel):
    dataprogress: Dict[str, str]
    type: Literal["Practice", "FullTest"]
    part: List[str]
    time: int
    test_id: int
    status: Literal["save", "submit"]
    time_left: Optional[int] = 0


class HistoryResultDetailResponse(BaseModel):
    history_id: int
    test_id: int
    test_type: str
    test_name: str
    correct_count: int
    incorrect_count: int
    correct_listening: int
    correct_reading: int
    no_answer: int
    total_question: int
    accuracy: float
    create_at: datetime
    duration: int
    dataprogress: Json[Dict[str, str]]
    part_list: List[str]


class HitoryResultListResponse(BaseModel):
    history_id: int
    score: str
    test_id: int
    test_type: str
    test_name: str
    duration: int
    part_list: List[str]
    create_at: datetime