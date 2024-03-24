from typing import Any

from base.schemas import OkSchema
from core.components import Request
from fastapi import APIRouter

from quiz.schemes import QuestionSchema

quiz_route = APIRouter(tags=["Quiz"])


@quiz_route.post(
    "/add_course_theme",
    summary="Add new theme to the database",
    description="Add new theme to the database",
    response_model=OkSchema,
)
async def add_course_theme(request: "Request", theme: str) -> Any:
    await request.app.store.quiz_manager.add_theme(theme)
    message = f"New theme added: {theme}"
    request.app.logger.info(message)
    return OkSchema(message=message)


@quiz_route.post(
    "/add_new_question",
    summary="Add new question to the database",
    description="Add new question to the database",
    response_model=OkSchema,
)
async def add_new_question(request: "Request", question: QuestionSchema) -> Any:
    await request.app.store.quiz_manager.add_question(**question.model_dump())
    message = f"New question added: {question}"
    request.app.logger.info(message)
    return OkSchema(message=message)
