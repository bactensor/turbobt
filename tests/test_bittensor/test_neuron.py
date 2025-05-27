import ipaddress
import pytest

from turbobt.neuron import AxonInfo, Neuron, PrometheusInfo
from turbobt.subnet import SubnetReference


@pytest.mark.asyncio
async def test_get(mocked_subtensor, bittensor):
    mocked_subtensor.neuron_info.get_neuron.return_value = {
        "hotkey": "5C4hrfjw9DjXZTzV3MwzrrAr9P1MJhSrvWGWqi1eSuyUpnhM",
        "coldkey": "5C4hrfjw9DjXZTzV3MwzrrAr9P1MJhSrvWGWqi1eSuyUpnhM",
        "uid": 0,
        "netuid": 1,
        "active": True,
        "axon_info": {
            "block": 0,
            "version": 0,
            "ip": 0,
            "port": 0,
            "ip_type": 0,
            "protocol": 0,
            "placeholder1": 0,
            "placeholder2": 0,
        },
        "prometheus_info": {
            "block": 0,
            "version": 0,
            "ip": 0,
            "port": 0,
            "ip_type": 0,
        },
        "stake": {
            "5C4hrfjw9DjXZTzV3MwzrrAr9P1MJhSrvWGWqi1eSuyUpnhM": 1000000000,
        },
        "rank": 0,
        "emission": 0,
        "incentive": 0,
        "consensus": 0,
        "trust": 0,
        "validator_trust": 0,
        "dividends": 0,
        "last_update": 0,
        "validator_permit": True,
        "weights": [],
        "bonds": [],
        "pruning_score": 65535,
    }

    subnet_ref = bittensor.subnet(1)
    neuron_ref = subnet_ref.neuron(0)
    neuron = await neuron_ref.get()

    assert neuron == Neuron(
        active=True,
        axon_info=AxonInfo(
            ip=ipaddress.IPv4Address("0.0.0.0"),
            port=0,
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
            ip=ipaddress.IPv4Address("0.0.0.0"),
            port=0,
        ),
        pruning_score=65535,
        rank=0,
        stake=1.0,
        subnet=SubnetReference(
            client=bittensor,
            netuid=1,
        ),
        trust=0,
        uid=0,
        validator_permit=True,
        validator_trust=0,
    )
