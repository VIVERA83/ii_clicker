from typing import Any

from icecream import ic

from clicker.schemes import OkSchema, QuestionSchema
from core.components import Request
from fastapi import APIRouter

clicker_route = APIRouter()


@clicker_route.post(
    "/add_course_theme",
    summary="test endpoint",
    description="test endpoint",
    response_model=OkSchema,
)
async def add_course_theme(request: "Request", theme: str) -> Any:
    await request.app.store.quiz_manager.add_theme(theme)
    message = f"New theme added: {theme}"
    request.app.logger.info(message)
    return OkSchema(message=message)


@clicker_route.post(
    "/add_new_question",
    summary="test endpoint",
    description="test endpoint",
    response_model=OkSchema,
)
async def add_new_question(request: "Request", question: QuestionSchema) -> Any:
    await request.app.store.quiz_manager.add_question(**question.model_dump())
    message = f"New question added: {question}"
    request.app.logger.info(message)
    return OkSchema(message=message)
