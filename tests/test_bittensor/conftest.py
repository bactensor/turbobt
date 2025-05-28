import unittest.mock

import pytest_asyncio

import turbobt


@pytest_asyncio.fixture
async def mocked_subtensor():
    with unittest.mock.patch(
        "turbobt.client.CacheSubtensor",
        return_value=unittest.mock.AsyncMock(),
    ) as subtensor:
        yield subtensor.return_value


@pytest_asyncio.fixture
async def bittensor(mocked_subtensor, alice_wallet):
    async with turbobt.Bittensor(
        "ws://127.0.0.1:9944",
        verify=None,
        wallet=alice_wallet,
    ) as client:
        yield client
