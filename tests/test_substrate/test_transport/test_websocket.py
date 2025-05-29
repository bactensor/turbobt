import asyncio
import unittest.mock

import pytest

from turbobt.substrate._models import Request
from turbobt.substrate.transports.websocket import WebSocketTransport


@pytest.mark.asyncio
@unittest.mock.patch("websockets.asyncio.client.connect")
async def test_concurrent_sends(mock_connect):
    transport = WebSocketTransport("ws://localhost:9944")
    connecting = asyncio.Semaphore(1)

    async def connect(*args, **kwargs):
        async with connecting:
            await asyncio.sleep(0)

        for future_id, future in transport._futures.items():
            future.set_result(
                {
                    "result": future_id,
                }
            )

        return unittest.mock.AsyncMock()

    mock_connect.return_value.__aenter__ = connect

    result1, result2 = await asyncio.gather(
        transport.send(
            Request(
                method="state_call",
                params={
                    "name": "state_getRuntimeVersion",
                },
            )
        ),
        transport.send(
            Request(
                method="state_call",
                params={
                    "name": "state_getRuntimeVersion",
                },
            )
        ),
    )

    assert result1.result == 1
    assert result2.result == 2
