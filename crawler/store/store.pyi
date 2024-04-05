from core.components import Application
from store.clicker.accessor import ClickerAccessor

class Store:
    """Store, data car and working with it."""

    clicker: ClickerAccessor

    def __init__(self, app: Application):
        """
        Initialize the store.

        Args:
            app (Application): The main application component.
        """

def setup_store(app: Application):
    app.store = Store(app)
