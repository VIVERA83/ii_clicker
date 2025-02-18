import asyncio

from clicker.execute_rpc_action import execute_rpc_action
from core.logger import setup_logging
from rpc.rpc_server import RPCServer


def run_rpc():
    """A function to run an RPC with the given RPCServer instance."""
    loop = asyncio.get_event_loop()
    logger = setup_logging()
    rpc_server = RPCServer(
        logger=logger,
        action=execute_rpc_action,
    )
    try:
        loop.run_until_complete(rpc_server.start())
    except KeyboardInterrupt:
        logger.warning("RPC server stopped")
