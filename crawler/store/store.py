"""A module describing services for working with data."""

from store.clicker.accessor import ClickerAccessor
from store.database.postgres import Postgres
from store.quiz.accessor import QuizAccessor
from store.quiz.manager import QuizManager


class Store:
    """Store, data car and working with it."""

    def __init__(self, app):
        """Initializing data sources.

        Args:
            app: The application
        """
        self.quiz = QuizAccessor(app)
        self.quiz_manager = QuizManager(app)

        self.clicker = ClickerAccessor(app)


def setup_store(app):
    """Configuring the connection and disconnection of storage.

    Here we inform the application about the databases of the database and other
    data sources which we run when the application is launched,
    and how to disable them.

    Args:
        app: The application
    """
    app.postgres = Postgres(app)
    app.store = Store(app)
