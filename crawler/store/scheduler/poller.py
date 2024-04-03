from asyncio import CancelledError, sleep
from datetime import datetime, timezone

from base.base_worker import BaseWorker
from core.settings import PollerSettings


class Poller(BaseWorker):
    """A worker that polls the Yandex Disk for new files and adds them to the scheduler queue.

    Attributes:
        settings (PollerSettings): The Poller settings.
    """

    settings: PollerSettings = None

    def _init(self):
        """Initialize additional settings."""
        self.settings = PollerSettings()
        self.last_update = datetime(
            year=2000, month=1, day=1, hour=0, tzinfo=timezone.utc
        )

    async def _worker(self):
        """The worker method.


        Raises:
            CancelledError: If the worker is cancelled.
        """
        message = f"{self.__class__.__name__} : {self.name} Last update "
        while self.is_running:
            creates = []
            try:
                async for file in await self.app.store.ya_disk.list_dir():
                    if self.last_update < file.created:
                        await self.app.store.scheduler.queue.put(file.name)
                        creates.append(file.created)
                if creates:
                    self.last_update = max(creates)
                    self.logger.info(message + str(self.last_update))
                await sleep(self.settings.timeout)
            except CancelledError:
                self.is_running = False
