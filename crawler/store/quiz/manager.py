from typing import Any
from uuid import uuid4

from base.base_accessor import BaseAccessor
from store.quiz.models import ThemeModel, QuestionModel, AnswerModel


class QuizManager(BaseAccessor):
    async def add_theme(self, theme: str):
        await self.app.store.quiz.create_or_update_many(
            model=ThemeModel,
            data=[{ThemeModel.title.name: theme}],
            index=[ThemeModel.title.name])

    async def add_question(self, title: str, theme: str, answers: list[dict[str, Any]]):
        question_id = uuid4().hex
        await self._add_question(title, theme, question_id)
        for answer in answers:
            await self._add_answer(question_id, **answer)

    async def _add_question(self, title: str, theme: str, question_id: str):
        await self.app.store.quiz.create_or_update_many(
            model=QuestionModel,
            data=[{QuestionModel.title.name: title,
                   QuestionModel.theme.name: theme,
                   QuestionModel.id.name: question_id}],
            index=[QuestionModel.id.name])

    async def _add_answer(self, id_question: str, title: str, is_correct: bool):
        answer_id = uuid4().hex
        await self.app.store.quiz.create_or_update_many(
            model=AnswerModel,
            data=[{AnswerModel.id.name: answer_id,
                   AnswerModel.id_question.name: id_question,
                   AnswerModel.title.name: title,
                   AnswerModel.is_correct.name: is_correct,
                   }],
            index=[AnswerModel.id.name])
