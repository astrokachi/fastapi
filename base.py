from pydantic import BaseModel
# from typing import List, Annotated

class Choice(BaseModel):
    choice_text: str
    is_correct: bool


class Question(BaseModel):
    question_text: str
    choices: list[Choice]