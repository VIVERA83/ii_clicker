from asyncio import CancelledError

from base.base_worker import BaseWorker


class Worker(BaseWorker):
    """Worker class that is responsible for processing data from the cloud and updating the database.

    Attributes:
        app (App): The main application object.
    """

    async def _worker(self):
        """The worker method that is executed in a separate thread.
        It continuously polls for new data from the cloud and processes it.
        """
        while self.is_running:
            try:
                1
            except CancelledError:
                self.is_running = False
