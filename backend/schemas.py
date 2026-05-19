from pydantic import BaseModel
from typing import Optional, List

class CandidateCreate(BaseModel):
    name: str
    email: Optional[str]
    domain: str

class AnswerIn(BaseModel):
    interview_id: int
    answer: str