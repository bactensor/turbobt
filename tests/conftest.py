import json
import tempfile
import unittest.mock

import bittensor_wallet
import pytest_asyncio

from tests.mock.transport import MockedTransport


@pytest_asyncio.fixture(scope="session")
def alice_wallet():
    keypair = bittensor_wallet.Keypair.create_from_uri("//Alice")

    wallet = bittensor_wallet.Wallet(
        path=tempfile.mkdtemp(),
    )
    wallet.set_coldkey(keypair=keypair, encrypt=False, overwrite=True)
    wallet.set_coldkeypub(keypair=keypair, encrypt=False, overwrite=True)
    wallet.set_hotkey(keypair=keypair, encrypt=False, overwrite=True)

    return wallet


@pytest_asyncio.fixture(scope="session")
async def metadata():
    with open("tests/test_substrate/data/metadata_at_version.json") as data:
        return json.load(data)


@pytest_asyncio.fixture(scope="session")
async def runtime():
    with open("tests/test_substrate/data/runtimeVersion.json") as data:
        return json.load(data)


@pytest_asyncio.fixture
async def mocked_transport(metadata, runtime):
    transport = MockedTransport()
    transport.responses["state_call"] = {
        "Metadata_metadata_at_version": {
            "result": metadata,
        },
    }
    transport.responses["state_getRuntimeVersion"] = {
        "result": runtime,
    }

    with unittest.mock.patch.object(transport, "send", wraps=transport.send):
        yield transport
