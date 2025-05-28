import ipaddress

import pytest

from turbobt.neuron import AxonInfo, Neuron, PrometheusInfo
from turbobt.subnet import Subnet, SubnetReference


@pytest.mark.asyncio
async def test_get(mocked_subtensor, bittensor):
    mocked_subtensor.subnet_info.get_dynamic_info.return_value = {
        "subnet_name": "apex",
        "token_symbol": "α",
        "owner_hotkey": "5C4hrfjw9DjXZTzV3MwzrrAr9P1MJhSrvWGWqi1eSuyUpnhM",
        "owner_coldkey": "5C4hrfjw9DjXZTzV3MwzrrAr9P1MJhSrvWGWqi1eSuyUpnhM",
        "tempo": 100,
        "subnet_identity": None,
    }

    subnet_ref = bittensor.subnet(1)
    subnet = await subnet_ref.get()

    assert subnet == Subnet(
        client=bittensor,
        identity=None,
        name="apex",
        netuid=1,
        owner_coldkey="5C4hrfjw9DjXZTzV3MwzrrAr9P1MJhSrvWGWqi1eSuyUpnhM",
        owner_hotkey="5C4hrfjw9DjXZTzV3MwzrrAr9P1MJhSrvWGWqi1eSuyUpnhM",
        symbol="α",
        tempo=100,
    )


@pytest.mark.asyncio
async def test_get_hyperparameters(mocked_subtensor, bittensor):
    mocked_subtensor.subnet_info.get_subnet_hyperparams.return_value = {
        "activity_cutoff": 5000,
        "adjustment_alpha": 0,
        "adjustment_interval": 100,
        "alpha_high": 58982,
        "alpha_low": 45875,
        "bonds_moving_avg": 900000,
        "commit_reveal_period": 1,
        "commit_reveal_weights_enabled": False,
        "difficulty": 10000000,
        "immunity_period": 4096,
        "kappa": 32767,
        "liquid_alpha_enabled": False,
        "max_burn": 100000000000,
        "max_difficulty": 4611686018427387903,
        "max_regs_per_block": 1,
        "max_validators": 64,
        "max_weights_limit": 1.0,
        "min_allowed_weights": 0,
        "min_burn": 500000,
        "min_difficulty": 10000000,
        "registration_allowed": True,
        "rho": 10,
        "serving_rate_limit": 50,
        "target_regs_per_interval": 2,
        "tempo": 100,
        "weights_rate_limit": 100,
        "weights_version": 0,
    }

    subnet_ref = bittensor.subnet(1)
    subnet_hyperparameters = await subnet_ref.get_hyperparameters()

    assert subnet_hyperparameters == {
        "activity_cutoff": 5000,
        "adjustment_alpha": 0,
        "adjustment_interval": 100,
        "alpha_high": 58982,
        "alpha_low": 45875,
        "bonds_moving_avg": 900000,
        "commit_reveal_period": 1,
        "commit_reveal_weights_enabled": False,
        "difficulty": 10000000,
        "immunity_period": 4096,
        "kappa": 32767,
        "liquid_alpha_enabled": False,
        "max_burn": 100000000000,
        "max_difficulty": 4611686018427387903,
        "max_regs_per_block": 1,
        "max_validators": 64,
        "max_weights_limit": 1.0,
        "min_allowed_weights": 0,
        "min_burn": 500000,
        "min_difficulty": 10000000,
        "registration_allowed": True,
        "rho": 10,
        "serving_rate_limit": 50,
        "target_regs_per_interval": 2,
        "tempo": 100,
        "weights_rate_limit": 100,
        "weights_version": 0,
    }


@pytest.mark.asyncio
async def test_get_state(mocked_subtensor, bittensor):
    mocked_subtensor.subnet_info.get_subnet_state.return_value = {
        "active": [True],
        "alpha_stake": [1000000000],
        "block_at_registration": [0],
        "coldkeys": ["5C4hrfjw9DjXZTzV3MwzrrAr9P1MJhSrvWGWqi1eSuyUpnhM"],
        "consensus": [0],
        "dividends": [0],
        "emission_history": [[0], [0]],
        "emission": [0],
        "hotkeys": ["5C4hrfjw9DjXZTzV3MwzrrAr9P1MJhSrvWGWqi1eSuyUpnhM"],
        "incentives": [0],
        "last_update": [0],
        "netuid": 1,
        "pruning_score": [65535],
        "rank": [0],
        "tao_stake": [0],
        "total_stake": [1000000000],
        "trust": [0],
        "validator_permit": [True],
    }

    subnet_ref = bittensor.subnet(1)
    subnet_state = await subnet_ref.get_state()

    assert subnet_state == {
        "active": [True],
        "alpha_stake": [1000000000],
        "block_at_registration": [0],
        "coldkeys": ["5C4hrfjw9DjXZTzV3MwzrrAr9P1MJhSrvWGWqi1eSuyUpnhM"],
        "consensus": [0],
        "dividends": [0],
        "emission_history": [[0], [0]],
        "emission": [0],
        "hotkeys": ["5C4hrfjw9DjXZTzV3MwzrrAr9P1MJhSrvWGWqi1eSuyUpnhM"],
        "incentives": [0],
        "last_update": [0],
        "netuid": 1,
        "pruning_score": [65535],
        "rank": [0],
        "tao_stake": [0],
        "total_stake": [1000000000],
        "trust": [0],
        "validator_permit": [True],
    }


@pytest.mark.asyncio
async def test_list_neurons(mocked_subtensor, bittensor):
    mocked_subtensor.neuron_info.get_neurons_lite.return_value = [
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

    subnet_ref = bittensor.subnet(1)
    subnet_neurons = await subnet_ref.list_neurons()

    assert subnet_neurons == [
        Neuron(
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
            pruning_score=0,
            rank=0,
            stake=1.0,
            subnet=SubnetReference(
                client=bittensor,
                netuid=1,
            ),
            trust=0,
            uid=0,
            validator_permit=False,
            validator_trust=0,
        ),
    ]


@pytest.mark.asyncio
async def test_list_validators(mocked_subtensor, bittensor):
    mocked_subtensor.chain.getBlockHash.return_value = (
        "0x2bb80cc429296b4da191bcec87d4b526ca0e407b4756f2a387a87d3b8e26ae42"
    )
    mocked_subtensor.subnet_info.get_subnet_state.return_value = {
        "active": [True],
        "alpha_stake": [1000000000],
        "block_at_registration": [0],
        "coldkeys": ["5C4hrfjw9DjXZTzV3MwzrrAr9P1MJhSrvWGWqi1eSuyUpnhM"],
        "consensus": [0],
        "dividends": [0],
        "emission_history": [[0], [0]],
        "emission": [0],
        "hotkeys": ["5C4hrfjw9DjXZTzV3MwzrrAr9P1MJhSrvWGWqi1eSuyUpnhM"],
        "incentives": [0],
        "last_update": [0],
        "netuid": 1,
        "pruning_score": [65535],
        "rank": [0],
        "tao_stake": [0],
        "total_stake": [1000000000],
        "trust": [0],
        "validator_permit": [True],
    }
    mocked_subtensor.subnet_info.get_subnet_hyperparams.return_value = {
        "activity_cutoff": 5000,
        "adjustment_alpha": 0,
        "adjustment_interval": 100,
        "alpha_high": 58982,
        "alpha_low": 45875,
        "bonds_moving_avg": 900000,
        "commit_reveal_period": 1,
        "commit_reveal_weights_enabled": False,
        "difficulty": 10000000,
        "immunity_period": 4096,
        "kappa": 32767,
        "liquid_alpha_enabled": False,
        "max_burn": 100000000000,
        "max_difficulty": 4611686018427387903,
        "max_regs_per_block": 1,
        "max_validators": 64,
        "max_weights_limit": 1.0,
        "min_allowed_weights": 0,
        "min_burn": 500000,
        "min_difficulty": 10000000,
        "registration_allowed": True,
        "rho": 10,
        "serving_rate_limit": 50,
        "target_regs_per_interval": 2,
        "tempo": 100,
        "weights_rate_limit": 100,
        "weights_version": 0,
    }
    mocked_subtensor.neuron_info.get_neurons_lite.return_value = [
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
    mocked_subtensor.state.getStorage.return_value = 1_000_000

    subnet_ref = bittensor.subnet(1)
    subnet_validators = await subnet_ref.list_validators()

    assert subnet_validators == [
        Neuron(
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
            pruning_score=0,
            rank=0,
            stake=1.0,
            subnet=SubnetReference(
                client=bittensor,
                netuid=1,
            ),
            trust=0,
            uid=0,
            validator_permit=False,
            validator_trust=0,
        ),
    ]


@pytest.mark.asyncio
async def test_register_subnet(mocked_subtensor, bittensor, alice_wallet):
    await bittensor.subnets.register(
        wallet=alice_wallet,
    )

    mocked_subtensor.subtensor_module.register_network.assert_awaited_once_with(
        hotkey="5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
        mechid=1,
        wallet=alice_wallet,
    )
