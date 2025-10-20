from datetime import datetime
from typing import Dict, List, Literal
from pydantic import BaseModel, Json


class HistoryResp(BaseModel):
    id: int
    dataprog: Json[Dict[str, str]]  # JSON field
    type: str                           # varchar(20) - "Practice", "FullTest", etc.
    part_id_list: Json[List[str]]               # JSON field - ["Part 5"]
    dura: float                          # int field
    test_id: int                        # bigint field
    user_id: int                        # bigint field  
    create_at: datetime                 # datetime field (note: create_at, not created_at)
    status: str                         # varchar(10) - "submit", etc.


class HistoryCreateReq(BaseModel):
    dataprog: Dict[str, str]
    type: Literal["Practice", "FullTest"]
    part_id_list: List[str]
    dura: float
    test_id: int
    status: Literal["save", "submit"]


class HistoryCreateResp(BaseModel):
    history_id: int
    status: str
    message: str

class HistoryResultDetailResp(BaseModel):
    history_id: int
    test_id: int
    test_type: str
    test_name: str
    correct_count: int
    incorrect_count: int
    correct_listening: int
    correct_reading: int
    no_ans: int
    total_ques: int
    accuracy: float
    dura: int
    create_at: datetime
    dataprog: Json[Dict[str, str]]
    part_id_list: List[str]


class HitoryResultListResp(BaseModel):
    history_id: int
    score: str
    test_id: int 
    test_type: str
    test_name: str
    dura: int
    part_id_list: List[str]
    part_order_list: List[str]
    create_at: datetime