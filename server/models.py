from pydantic import BaseModel
from typing import List


class QA(BaseModel):
    question: str
    answer: str


class CONFIG_JSON(BaseModel):
    name: str
    question_answers: List[QA]


class GPTRequest(BaseModel):
    instruction: str
    user_input: str
