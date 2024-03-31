from typing import Literal

from pydantic import BaseModel, Field

COURSE_NAMES = Literal["Защитное Вождение", "Экономическое Вождение"]


class CourseSchema(BaseModel):
    login: str = Field(description="Your login", example="ivanov")
    password: str = Field(description="Your password", example="mypass")
    course: list[COURSE_NAMES] = Field(description="Your course", example=["Защитное Вождение"])
