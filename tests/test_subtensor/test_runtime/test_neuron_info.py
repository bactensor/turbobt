import pytest


@pytest.mark.asyncio
async def test_get_neuron(subtensor, mocked_transport):
    mocked_transport.responses["state_call"]["NeuronInfoRuntimeApi_get_neuron"] = {
        "result": "0x0100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000401000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000002286bee0000000000000000010000feff0300",
    }

    neuron = await subtensor.neuron_info.get_neuron(
        netuid=1,
        uid=0,
    )

    assert neuron == {
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


@pytest.mark.asyncio
async def test_get_neuron_uid_not_found(subtensor, mocked_transport):
    mocked_transport.responses["state_call"]["NeuronInfoRuntimeApi_get_neuron"] = {
        "result": "0x00",
    }

    neuron = await subtensor.neuron_info.get_neuron(
        netuid=1,
        uid=404,
    )

    assert neuron is None


@pytest.mark.asyncio
async def test_get_neuron_netuid_not_found(subtensor, mocked_transport):
    mocked_transport.responses["state_call"]["NeuronInfoRuntimeApi_get_neuron"] = {
        "result": "0x00",
    }

    neuron = await subtensor.neuron_info.get_neuron(
        netuid=404,
        uid=0,
    )

    assert neuron is None


@pytest.mark.asyncio
async def test_get_neurons_lite(subtensor, mocked_transport):
    mocked_transport.responses["state_call"][
        "NeuronInfoRuntimeApi_get_neurons_lite"
    ] = {
        "result": "0x0400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000401000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000002286bee00000000000000000000",
    }

    neurons = await subtensor.neuron_info.get_neurons_lite(
        netuid=1,
    )

    assert neurons == [
        {
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
            "validator_permit": False,
            "pruning_score": 0,
        },
    ]


@pytest.mark.asyncio
async def test_get_neurons_lite_not_found(subtensor, mocked_transport):
    mocked_transport.responses["state_call"][
        "NeuronInfoRuntimeApi_get_neurons_lite"
    ] = {
        "result": "0x00",
    }

    neurons = await subtensor.neuron_info.get_neurons_lite(
        netuid=404,
    )

    assert neurons is None
