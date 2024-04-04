from clicker.views import clicker_route
from core.components import Application


def setup_routes(app: Application):
    """Configuring the connected routes to the application."""
    app.include_router(clicker_route)
