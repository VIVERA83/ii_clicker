from clicker.views import clicker_route
from core.components import Application
from quiz.views import quiz_route


def setup_routes(app: Application):
    """Configuring the connected routes to the application."""
    app.include_router(clicker_route)
    app.include_router(quiz_route)
