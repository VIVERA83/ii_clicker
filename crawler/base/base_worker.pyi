from asyncio import Task
from logging import Logger

from core.components import Application

class BaseWorker:
    name: str = "Worker"
    app: Application
    logger: Logger
    task: Task
    is_running: bool

    def __init__(self, app: Application, name: str = "Worker"):
        self._init()

    def _init(self):
        pass

    async def start(self): ...
    async def stop(self): ...
    async def _worker(self):
        raise NotImplementedError()
