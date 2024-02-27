from core.components import Application


class Store:
    """Store, data car and working with it."""

    def __init__(self, app: Application):
        """
        Initialize the store.

        Args:
            app (Application): The main application component.
        """


def setup_store(app: Application):
    app.store = Store(app)
