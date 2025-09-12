import ipaddress

import pytest_asyncio

import turbobt
from turbobt.neuron import AxonInfo, Neuron, PrometheusInfo
from turbobt.subnet import SubnetReference


@pytest_asyncio.fixture
async def mocked_subtensor(mocker):
    mock_subtensor = mocker.AsyncMock()
    mocker.patch(
        "turbobt.client.CacheSubtensor",
        return_value=mock_subtensor,
    )
    yield mock_subtensor


@pytest_asyncio.fixture
async def bittensor(mocked_subtensor, alice_wallet):
    async with turbobt.Bittensor(
        "ws://127.0.0.1:9944",
        verify=None,
        wallet=alice_wallet,
    ) as client:
        yield client


@pytest_asyncio.fixture
async def neuron(bittensor):
    return Neuron(
        active=True,
        axon_info=AxonInfo(
            ip=ipaddress.IPv4Address("192.168.1.1"),
            port=8080,
            protocol=0,
        ),
        coldkey="5C4hrfjw9DjXZTzV3MwzrrAr9P1MJhSrvWGWqi1eSuyUpnhM",
        consensus=0,
        dividends=0,
        emission=0,
        hotkey="5C4hrfjw9DjXZTzV3MwzrrAr9P1MJhSrvWGWqi1eSuyUpnhM",
        incentive=0,
        last_update=0,
        prometheus_info=PrometheusInfo(
            ip=ipaddress.IPv4Address("192.168.1.1"),
            port=9090,
        ),
        pruning_score=0,
        rank=0,
        stake=1.0,
        subnet=SubnetReference(client=bittensor, netuid=1),
        trust=0,
        uid=0,
        validator_permit=False,
        validator_trust=0,
    )
