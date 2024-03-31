from typing import Any

from fastapi import APIRouter

from base.schemas import OkSchema
from clicker.schemes import CourseSchema
from core.components import Request
from store.clicker.help import help_dict
from store.clicker.rename import ProtectiveDrivingCourse

clicker_route = APIRouter(tags=["Clicker"])


@clicker_route.post(
    "/auto_scroll_course",
    summary="Auto scroll course",
    description="Complete the set course in automatic mode",
    response_model=OkSchema,
)
async def auto_scroll_course(request: "Request", course: CourseSchema) -> Any:
    request.app.logger.info(f"Add new course: {course}")
    magnum = ProtectiveDrivingCourse(course.login, course.password,
                                     "hello world",
                                     help_dict,
                                     min_sec_answer=5,
                                     max_sec_answer=10,
                                     logger=request.app.logger)
    try:
        magnum.start_course()
    except Exception as ex:
        raise Exception(ex.args[0])
    finally:
        magnum.driver.quit()
    return OkSchema(message="Course completed successfully")
