import unittest.mock

import pytest_asyncio

import turbobt


@pytest_asyncio.fixture
async def subtensor(mocked_transport):
    async with turbobt.Subtensor(
        "ws://127.0.0.1:9944",
        transport=mocked_transport,
        verify=None,
    ) as subtensor:
        with unittest.mock.patch.object(subtensor, "author", wraps=subtensor.author):
            yield subtensor
