import asyncio
from typing import Literal

from clicker.clicker import CourseClicker
from clicker.courses import (
    DriverCourseType,
    DispatcherCourseType,
    MentorCourseType,
    RatingCourseType,
    TrainingCourse,
    CourseType,
)
from core.logger import setup_logging

from rpc.rpc_server import RPCServer
from temp.crawler.clicker.schemes import CourseTypeEnum

courses = {
    CourseTypeEnum.driver.value: DriverCourseType,
    CourseTypeEnum.dispatcher.value: DispatcherCourseType,
    CourseTypeEnum.mentor.value: MentorCourseType,
    CourseTypeEnum.rating.value: RatingCourseType,
}

COURSE_TYPE = Literal["cpd", "epd", "etd", "d", "n", "z", "ce", "ee"]

def get_courses_by_type(course_type: Literal[]):

async def program(
    login: str, password: str, course_type: str):

    course: list[CourseTypeEnum]

    type_course = courses.get(course_type)
    logger = setup_logging()
    logger.info(f"Start {course_type} course, user: {login}")
    for ce in course:
        clicker = CourseClicker(
            login=login,
            password=password,
            training_course=TrainingCourse(type_course, CourseType(ce)),
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


def run_rpc():
    rpc_server = RPCServer(
        logger=setup_logging(),
        program=program,
    )
    asyncio.run(rpc_server.start())
