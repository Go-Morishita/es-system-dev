from pydantic import BaseModel


class CONFIG_JSON(BaseModel):
    name: str
    question1: str
    answer1: str
    question2: str
    answer2: str


class GPTRequest(BaseModel):
    instruction: str
    user_input: str
