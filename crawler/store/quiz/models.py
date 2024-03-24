from typing import Union, Type
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from store.database.postgres import Base

MODEL = Union[Type["ThemeModel"], Type["QuestionModel"], Type["AnswerModel"]]


class ThemeModel(Base):
    __tablename__ = "themes"

    title: Mapped[str] = mapped_column(unique=True, init=False)
    questions = relationship(
        "QuestionModel", back_populates="theme", cascade="all, delete", passive_deletes=True,
    )


class QuestionModel(Base):
    """Course model."""

    __tablename__ = "questions"  # noqa

    theme: Mapped[str] = mapped_column(ForeignKey("themes.title", ondelete="CASCADE"), init=False)
    title: Mapped[str] = mapped_column(init=False)
    answers: Mapped[list["AnswerModel"]] = relationship(
        "ThemeModel", back_populates="questions", cascade="all, delete", passive_deletes=True, init=False
    )


class AnswerModel(Base):
    __tablename__ = "answers"  # noqa

    title: Mapped[str] = mapped_column(init=False)
    is_correct: Mapped[bool] = mapped_column(default=False, server_default="false", init=False)
    id_question: Mapped[UUID] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"), init=False)
