import pytest_asyncio

import turbobt


@pytest_asyncio.fixture
async def substrate(mocked_transport):
    async with turbobt.Substrate(
        "ws://127.0.0.1:9944",
        transport=mocked_transport,
        verify=None,
    ) as substrate:
        yield substrate
