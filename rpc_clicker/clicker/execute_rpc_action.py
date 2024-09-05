import json
from dataclasses import asdict, dataclass, field
from typing import Literal

from clicker.clicker import CourseClicker
from clicker.courses import (
    Course,
    CourseType,
    DispatcherCourseType,
    DriverCourseType,
    MentorCourseType,
    RatingCourseType,
    TrainingCourse,
)
from core.logger import setup_logging
from core.settings import ClickerSettings

COURSE_TYPE = Literal["cpd", "epd", "etd", "d", "m", "z", "ce", "ee"]


@dataclass
class Result:
    status: Literal["OK", "ERROR"] = "Ok"
    course: str = ""
    result: list = field(default_factory=list)
    message: str = "Успешно"

    def to_dict(self):
        return asdict(self)


def get_courses_by_type(course_type: COURSE_TYPE) -> Course:
    """A function to get courses based on the course type provided.

    Parameters:
    - course_type: The type of course to retrieve

    Returns:
    - Course: The course object corresponding to the provided course type or None if not found
    """
    return {
        "cpd": Course(
            type=DriverCourseType,
            courses=[
                CourseType.eco_small,
                CourseType.protective_driving,
                CourseType.final_test_c_pd,
            ],
        ),
        "epd": Course(
            type=DriverCourseType,
            courses=[
                CourseType.eco_full,
                CourseType.protective_driving,
                CourseType.final_test_e_pd,
            ],
        ),
        "etd": Course(
            type=DriverCourseType,
            courses=[
                CourseType.eco_full,
                CourseType.protective_driving,
                CourseType.final_test_e_td,
            ],
        ),
        "d": Course(
            type=DispatcherCourseType,
            courses=[
                CourseType.eco_full,
                CourseType.eco_small,
                CourseType.protective_driving,
                CourseType.final_test_dispatcher,
            ],
        ),
        "m": Course(
            type=MentorCourseType,
            courses=[
                CourseType.eco_full,
                CourseType.eco_small,
                CourseType.protective_driving,
                CourseType.final_test_mentor,
            ],
        ),
        "z": Course(
            type=RatingCourseType,
            courses=[
                CourseType.protective_driving,
            ],
        ),
        "ce": Course(
            type=RatingCourseType,
            courses=[
                CourseType.eco_small,
            ],
        ),
        "ee": Course(
            type=RatingCourseType,
            courses=[
                CourseType.eco_full,
            ],
        ),
    }.get(course_type, None)


def get_course_name_by_type(course_type: COURSE_TYPE) -> str:
    return {
        "cpd": "Программа Водитель-экспедитор С ПД",
        "epd": "Программа Водитель-экспедитор E ПД",
        "etd": "Программа Водитель-экспедитор E ТД",
        "d": "Программа Водитель-диспетчер",
        "m": "Программа Водитель наставник",
        "z": "Программа Защитное вождение",
        "ce": "Программа Эко вождение малый формат",
        "ee": "Программа Эко вождение полный формат",
    }.get(course_type, "Неизвестный тип курса")


async def execute_rpc_action(
    login: str, password: str, course_type: COURSE_TYPE
) -> str:
    """Asynchronously runs a program for a specific course type.

    Parameters:
    - login (str): The login username.
    - password (str): The password for the login.
    - course_type (COURSE_TYPE): The type of course to run.
    Raises:
    - Exception: If the course is not found.
    Returns:
    - None
    """
    result = Result(course=get_course_name_by_type(course_type))
    setting = ClickerSettings()
    if course := get_courses_by_type(course_type):
        for c in course.courses:
            clicker = CourseClicker(
                login=login,
                password=password,
                training_course=TrainingCourse(course.type, c),
                logger=setup_logging(),
                min_sec=setting.min_sec,
                max_sec=setting.min_sec,
                min_sec_answer=setting.min_sec_answer,
                max_sec_answer=setting.max_sec_answer,
            )
            try:
                result.result.append({c.value: await clicker.start_course()})
            except Exception as ex:
                raise Exception(ex.args[0])
            finally:
                clicker.driver.quit()
        return json.dumps(result.to_dict())
    else:
        return json.dumps(
            Result(
                status="ERROR",
                course=course_type,
                result=[],
                message="Неизвестный тип курса",
            ).to_dict()
        )
