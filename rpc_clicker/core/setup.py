import asyncio
from dataclasses import dataclass
from typing import Literal

from clicker.clicker import CourseClicker
from clicker.courses import (
    TRAINING_TYPE,
    CourseType,
    DispatcherCourseType,
    DriverCourseType,
    MentorCourseType,
    RatingCourseType,
    TrainingCourse,
)
from core.logger import setup_logging
from rpc.rpc_server import RPCServer

COURSE_TYPE = Literal["cpd", "epd", "etd", "d", "m", "z", "ce", "ee"]


@dataclass
class Course:
    type: TRAINING_TYPE
    courses: list[CourseType]


def get_courses_by_type(course_type: COURSE_TYPE) -> Course:
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


async def program(login: str, password: str, course_type: COURSE_TYPE):
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
                await clicker.start_course()
            except Exception as ex:
                raise Exception(ex.args[0])
            finally:
                clicker.driver.quit()
    else:
        raise Exception("Course not found")


def run_rpc():
    rpc_server = RPCServer(
        logger=setup_logging(),
        program=program,
    )
    asyncio.run(rpc_server.start())
