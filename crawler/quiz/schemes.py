from typing import Literal

from pydantic import BaseModel

TEST_NAMES = Literal["Защитное вождение", "Экономическое вождение"]


class QuestionSchema(BaseModel):
    title: str
    theme: str
    answers: list["AnswerSchema"]


class AnswerSchema(BaseModel):
    title: str
    is_correct: bool
