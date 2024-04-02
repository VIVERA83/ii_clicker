from typing import Any

from base.schemas import OkSchema
from clicker.schemes import CourseSchema
from core.components import Request
from fastapi import APIRouter

clicker_route = APIRouter(tags=["Clicker"])


@clicker_route.post(
    "/auto_scroll_course",
    summary="Auto scroll course",
    description="Complete the set course in automatic mode",
    response_model=OkSchema,
)
async def auto_scroll_course(request: "Request", course: CourseSchema) -> Any:
    request.app.logger.info(f"Add new course: {course.course_type.value}")
    await request.app.store.clicker.start_clicker(**course.model_dump())
    return OkSchema(message="Course completed successfully")
