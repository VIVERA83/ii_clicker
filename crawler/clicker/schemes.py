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


class OkSchema(BaseModel):
    """
    Pydantic model for returning a successful status response.

    This class defines a Pydantic model for returning a successful status
    response. The model includes two fields: status, which indicates the
    status of the response (always "Ok" in this case), and message, which
    provides a brief message describing the outcome of the request.

    Attributes:
        status (str): The status of the response. Always "Ok" in this case.
        message (str): A brief message describing the outcome of the request.
    """

    status: str = "Оk"
    message: str = (
        "The data has been successfully added to the processing queue,"
        " and the results will be sent in a telegram."
    )
