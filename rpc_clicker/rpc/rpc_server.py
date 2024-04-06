import asyncio
import json
import logging

from aio_pika import Message, connect
from aio_pika.abc import (
    AbstractChannel,
    AbstractConnection,
    AbstractExchange,
    AbstractIncomingMessage,
    AbstractQueue,
)


class RPCServer:
    connection: AbstractConnection
    channel: AbstractChannel
    exchange: AbstractExchange
    queue: AbstractQueue

    def __init__(
        self, program, logger: logging.Logger = logging.getLogger(__name__)
    ) -> None:
        self.dns = "amqp://guest:guest@localhost/"
        self.queue_name = "rpc_queue"
        self.program = program
        self.logger = logger

    async def start(self) -> None:
        await self._connect()
        self.logger.info("Start RPC server")
        try:
            async with self.queue.iterator() as queue_iterator:
                message: AbstractIncomingMessage

                async for message in queue_iterator:

                    async with message.process(requeue=False):
                        try:
                            assert message.reply_to is not None
                            response = await self._execute_program(message.body)
                        except Exception as e:
                            self.logger.exception(
                                "Processing error for message ",
                            )
                            await self._reply_to(message, str(e).encode("utf-8"))
                            continue
                        await self._reply_to(message, str(response).encode("utf-8"))

        except asyncio.CancelledError:
            print(" [x] Canceled")
        finally:
            await self.connection.close()

    async def _reply_to(
        self, message: AbstractIncomingMessage, response: bytes
    ) -> None:
        await self.exchange.publish(
            Message(
                body=response,
                correlation_id=message.correlation_id,
            ),
            routing_key=message.reply_to,
        )
        self.logger.debug(f" [x] Sent {response!r}")

    async def _connect(self) -> "RPCServer":
        self.connection = await connect(self.dns)
        self.channel = await self.connection.channel()
        self.exchange = self.channel.default_exchange
        self.queue = await self.channel.declare_queue(self.queue_name)
        return self

    async def _execute_program(self, params: bytes) -> bytes:
        data = json.loads(params.decode("utf-8"))
        return await self.program(**data)
