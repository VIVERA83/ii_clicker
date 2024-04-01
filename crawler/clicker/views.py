from typing import Any

from base.schemas import OkSchema
from clicker.schemes import CourseSchema
from core.components import Request
from fastapi import APIRouter

from store.clicker.courses import TrainingCourse, RatingCourseType, CourseType
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
    magnum = CourseClicker(
        course.login,
        course.password,
        training_course=TrainingCourse(RatingCourseType, CourseType.protective_driving),
        min_sec_answer=5,
        max_sec_answer=10,
        logger=request.app.logger,
    )
    try:
        magnum.start_course()
    except Exception as ex:
        raise Exception(ex.args[0])
    finally:
        magnum.driver.quit()
    return OkSchema(message="Course completed successfully")
