import asyncio
from asyncio import Task
from typing import Optional


class BaseWorker:
    def __init__(self, app, name: str = "Worker"):
        self.name = name
        self.app = app
        self.logger = app.logger
        self.is_running = False
        self.task: Optional[Task] = None
        self._init()

    def _init(self):
        pass

    async def start(self):
        self.is_running = True
        self.task = asyncio.create_task(self._worker())
        self.logger.info(f"{self.__class__.__name__} : {self.name} started")

    async def stop(self):
        self.is_running = False
        if self.task:
            self.task.cancel()
        self.logger.info(f"{self.__class__.__name__} : {self.name} stopped")

    async def _worker(self):
        raise NotImplementedError()
