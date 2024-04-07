import asyncio

from clicker.execute_rpc_action import execute_rpc_action
from core.logger import setup_logging
from rpc.rpc_server import RPCServer


def run_rpc():
    """A function to run an RPC with the given RPCServer instance."""

    rpc_server = RPCServer(
        logger=setup_logging(),
        action=execute_rpc_action,
    )
    asyncio.run(rpc_server.start())
