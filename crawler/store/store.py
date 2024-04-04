"""A module describing services for working with data."""

from store.clicker.accessor import ClickerAccessor


class Store:
    """Store, data car and working with it."""

    def __init__(self, app):
        """Initializing data sources.

        Args:
            app: The application
        """

        self.clicker = ClickerAccessor(app)


def setup_store(app):
    """Configuring the connection and disconnection of storage.

    Here we inform the application about the databases of the database and other
    data sources which we run when the application is launched,
    and how to disable them.

    Args:
        app: The application
    """
    app.store = Store(app)
