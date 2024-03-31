from typing import Any

from base.base_accessor import BaseAccessor
from store.quiz.models import MODEL


class QuizAccessor(BaseAccessor):

    async def create_or_update_many(
        self, model: MODEL, data: list[dict[str, Any]], index: list[str]
    ):
        """
        Create multiple records in the database.

        Args:
            model (MODEL): The SQLAlchemy model class corresponding to the tables.
            data (list[dict[str, Any]]): A list of dictionaries containing the data for each record to be created.
            index: (list[str]): Table indexes
            The keys of each dictionary should match the column names of the model table.
        """
        query = [
            self.app.postgres.get_query_insert(
                model, **data_fields
            ).on_conflict_do_update(
                index_elements=index[:1],
                where=getattr(model, index[-1]).is_(None),
                set_={key: data_fields[key] for key in index},
            )
            for data_fields in data
        ]
        await self.app.postgres.query_executes(*query)
