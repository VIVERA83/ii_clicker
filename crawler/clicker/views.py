from typing import Any

from base.schemas import OkSchema
from clicker.schemes import CourseSchema, CourseTypeEnum
from core.components import Request
from fastapi import APIRouter

from store.clicker.courses import (
    TrainingCourse,
    RatingCourseType,
    DriverCourseType,
    DispatcherCourseType,
    MentorCourseType,
)
from store.clicker.rename import CourseClicker

clicker_route = APIRouter(tags=["Clicker"])


@clicker_route.post(
    "/auto_scroll_course",
    summary="Auto scroll course",
    description="Complete the set course in automatic mode",
    response_model=OkSchema,
)
async def auto_scroll_course(request: "Request", course: CourseSchema) -> Any:
    request.app.logger.info(f"Add new course: {course}")

    course_type = {
        CourseTypeEnum.driver.value: DriverCourseType,
        CourseTypeEnum.dispatcher.value: DispatcherCourseType,
        CourseTypeEnum.mentor.value: MentorCourseType,
        CourseTypeEnum.rating.value: RatingCourseType,
    }.get(course.course_type.value)
    for c in course.course:
        clicker = CourseClicker(
            course.login,
            course.password,
            training_course=TrainingCourse(course_type, c),
            min_sec_answer=5,
            max_sec_answer=10,
            logger=request.app.logger,
        )
        try:
            clicker.start_course()
        except Exception as ex:
            raise Exception(ex.args[0])
        finally:
            clicker.driver.quit()
    return OkSchema(message="Course completed successfully")
