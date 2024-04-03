from enum import Enum

from pydantic import BaseModel, Field


class CourseTypeEnum(Enum):
    driver = "стажировка водителя-экспедитора"
    dispatcher = "стажировка водителя-диспетчера"
    mentor = "стажировка наставника"
    rating = "по рейтингу"


class CourseEnum(Enum):
    eco_full = "Эко вождение полный формат"
    eco_small = "Эко вождение малый формат"
    protective_driving = "Защитное вождение"
    final_test_c_pd = "Итоговый тест водителя экспедитора С ПД"
    final_test_e_pd = "Итоговый тест водителя экспедитора E ПД"
    final_test_e_td = "Итоговый тест водителя экспедитора E ТД"
    final_test_dispatcher = "Итоговый тест водителя диспетчера"
    final_test_mentor = "Итоговый тест водителя наставника"


class CourseSchema(BaseModel):
    login: str = Field(description="Your login", example="ivanov")
    password: str = Field(description="Your password", example="mypass")
    course_type: CourseTypeEnum
    courses: list[CourseEnum]
