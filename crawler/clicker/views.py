from typing import Any

from fastapi import APIRouter
from icecream import ic

from base.schemas import OkSchema
from clicker.schemes import CourseSchema
from core.components import Request
from store.clicker.rename import ProtectiveDrivingCourse

clicker_route = APIRouter(tags=["Clicker"])


@clicker_route.post(
    "/auto_scroll_course",
    summary="Auto scroll course",
    description="Complete the set course in automatic mode",
    response_model=OkSchema,
)
async def auto_scroll_course(request: "Request", course: CourseSchema) -> Any:
    course = {"login": "sergievskiy_an",
              "password": "QQQQqqqq5555",
              "course": "Защитное Вождение"}
    message = f": {course}"
    request.app.logger.info(message)
    username = "sergievskiy_an"
    password = "QQQQqqqq5555"
    magnum = ProtectiveDrivingCourse(username, password, "hello world")
    try:
        magnum.start_course()
    except Exception as ex:
        ic(ex)
    finally:
        magnum.driver.quit()

    return OkSchema(message=message)
