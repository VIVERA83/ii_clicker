from enum import Enum

from pydantic import BaseModel, Field
from store.clicker.courses import CourseType


class CourseTypeEnum(Enum):
    driver = "стажировка водителя-экспедитора"
    dispatcher = "стажировка водителя-диспетчера"
    mentor = "стажировка наставника"
    rating = "по рейтингу"


class CourseSchema(BaseModel):
    login: str = Field(description="Your login", example="ivanov")
    password: str = Field(description="Your password", example="mypass")
    course_type: CourseTypeEnum
    courses: list[CourseType] = Field(
        description="Your course",
        example=[
            CourseType.eco_small,
            CourseType.protective_driving,
            CourseType.final_test_c_pd,
        ],
    )
