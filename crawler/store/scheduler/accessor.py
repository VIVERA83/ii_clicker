import asyncio
from asyncio import Queue

from base.base_accessor import BaseAccessor
from core.settings import SchedulerSettings
from store.scheduler.poller import Poller
from store.scheduler.worker import Worker


class SchedulerAccessor(BaseAccessor):
    """The SchedulerAccessor class is responsible for managing the scheduler.

    Args:
        app (Fast API): The FastAPI application.

    Attributes:
        settings (SchedulerSettings): The scheduler settings.
        queue (Queue[str]): A queue for storing file paths on a virtual disk that workers work with.
        poller (Poller): A questionnaire that fills the queue with files that the workers will work with.
        workers (list[Worker]): The workers for processing queries.
    """

    settings: SchedulerSettings
    queue: Queue
    poller: Poller
    workers: list[Worker]

    def _init(self):
        """This method initializes the scheduler.

        It creates the settings, queue instances.
        """
        self.settings = SchedulerSettings()
        self.queue = Queue(self.settings.queue_size)
        self.workers = []

    async def connect(self):
        """This method starts the poller and worker processes."""

        self.poller = Poller(self.app, "Poller_1")
        await self.poller.start()
        self.workers = [
            Worker(self.app, f"Worker_{i + 1}") for i in range(self.settings.worker)
        ]
        await asyncio.gather(*[worker.start() for worker in self.workers])
        self.logger.info(f"{self.__class__.__name__} connected")

    async def disconnect(self):
        """This method stops the poller and worker processes."""

        await self.poller.stop()
        await asyncio.gather(*[worker.stop() for worker in self.workers])
        self.logger.info(f"{self.__class__.__name__} disconnected")
