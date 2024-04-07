import json
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

COURSE_TYPE = Literal["cpd", "epd", "etd", "d", "m", "z", "ce", "ee"]


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
    result = {}
    if course := get_courses_by_type(course_type):
        for c in course.courses:
            clicker = CourseClicker(
                login=login,
                password=password,
                training_course=TrainingCourse(course.type, c),
                min_sec_answer=5,
                max_sec_answer=10,
                logger=setup_logging(),
            )
            try:
                result.update({c.value: await clicker.start_course()})
            except Exception as ex:
                raise Exception(ex.args[0])
            finally:
                clicker.driver.quit()
        return json.dumps(result)
    else:
        return json.dumps({"error": "Курс не найден"})
