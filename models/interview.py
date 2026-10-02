from pydantic import BaseModel
from typing import List


class Answer(BaseModel):
    question_number: int
    question: str
    answer: str
    evaluation: str = ""


class InterviewSession(BaseModel):
    session_id: str
    questions: List[str] = []
    answers: List[Answer] = []
    current_question_index: int = 0
    status: str = "in_progress"