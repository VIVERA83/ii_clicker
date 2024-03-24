from core.components import Application
from store.quiz.accessor import QuizAccessor
from store.quiz.manager import QuizManager


class Store:
    """Store, data car and working with it."""
    quiz: QuizAccessor
    quiz_manager: QuizManager

    def __init__(self, app: Application):
        """
        Initialize the store.

        Args:
            app (Application): The main application component.
        """


def setup_store(app: Application):
    app.store = Store(app)
