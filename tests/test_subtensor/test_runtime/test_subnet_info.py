import pytest


@pytest.mark.asyncio
async def test_get_dynamic_info(subtensor, mocked_transport):
    mocked_transport.responses["state_call"][
        "SubnetInfoRuntimeApi_get_dynamic_info"
    ] = {
        "result": "0x010400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000108501c1019501e101083903c5029101bd0f10000700e40b540202286bee0700e40b5402000000000000000000000000000000000000000000000000",
    }

    dynamic_info = await subtensor.subnet_info.get_dynamic_info(
        netuid=1,
    )

    assert dynamic_info == {
        "netuid": 1,
        "owner_hotkey": "5C4hrfjw9DjXZTzV3MwzrrAr9P1MJhSrvWGWqi1eSuyUpnhM",
        "owner_coldkey": "5C4hrfjw9DjXZTzV3MwzrrAr9P1MJhSrvWGWqi1eSuyUpnhM",
        "subnet_name": "apex",
        "token_symbol": "α",
        "tempo": 100,
        "last_step": 1007,
        "blocks_since_last_step": 4,
        "emission": 0,
        "alpha_in": 10000000000,
        "alpha_out": 1000000000,
        "tao_in": 10000000000,
        "alpha_out_emission": 0,
        "alpha_in_emission": 0,
        "tao_in_emission": 0,
        "pending_alpha_emission": 0,
        "pending_root_emission": 0,
        "subnet_volume": 0,
        "network_registered_at": 0,
        "subnet_identity": None,
        "moving_price": {
            "bits": 0,
        },
    }


@pytest.mark.asyncio
async def test_get_dynamic_info_not_found(subtensor, mocked_transport):
    mocked_transport.responses["state_call"][
        "SubnetInfoRuntimeApi_get_dynamic_info"
    ] = {
        "result": "0x00",
    }

    dynamic_info = await subtensor.subnet_info.get_dynamic_info(
        netuid=404,
    )

    assert dynamic_info is None


@pytest.mark.asyncio
async def test_get_subnet_hyperparams(subtensor, mocked_transport):
    mocked_transport.responses["state_call"][
        "SubnetInfoRuntimeApi_get_subnet_hyperparams"
    ] = {
        "result": "0x0128feff0100014000feff03009101025a620213ffffffffffffff3f0091019101214e010882841e000700e876481782ee360004c8010100025a620204009a990300cecc020000",
    }

    subnet_hyperparams = await subtensor.subnet_info.get_subnet_hyperparams(
        netuid=1,
    )

    assert subnet_hyperparams == {
        "rho": 10,
        "kappa": 32767,
        "immunity_period": 4096,
        "min_allowed_weights": 0,
        "max_weights_limit": 1.0,
        "tempo": 100,
        "min_difficulty": 10000000,
        "max_difficulty": 4611686018427387903,
        "weights_version": 0,
        "weights_rate_limit": 100,
        "adjustment_interval": 100,
        "activity_cutoff": 5000,
        "registration_allowed": True,
        "target_regs_per_interval": 2,
        "min_burn": 500000,
        "max_burn": 100000000000,
        "bonds_moving_avg": 900000,
        "max_regs_per_block": 1,
        "serving_rate_limit": 50,
        "max_validators": 64,
        "adjustment_alpha": 0,
        "difficulty": 10000000,
        "commit_reveal_period": 1,
        "commit_reveal_weights_enabled": False,
        "alpha_high": 58982,
        "alpha_low": 45875,
        "liquid_alpha_enabled": False,
    }


@pytest.mark.asyncio
async def test_get_subnet_hyperparams_not_found(subtensor, mocked_transport):
    mocked_transport.responses["state_call"][
        "SubnetInfoRuntimeApi_get_subnet_hyperparams"
    ] = {
        "result": "0x00",
    }

    subnet_hyperparams = await subtensor.subnet_info.get_subnet_hyperparams(
        netuid=404,
    )

    assert subnet_hyperparams is None


@pytest.mark.asyncio
async def test_get_subnet_state(subtensor, mocked_transport):
    mocked_transport.responses["state_call"][
        "SubnetInfoRuntimeApi_get_subnet_state"
    ] = {
        "result": "0x01040400000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000000401040104feff0300040004000400040004000400040004000402286bee04000402286bee0804000400",
    }

    subnet_state = await subtensor.subnet_info.get_subnet_state(
        netuid=1,
    )

    assert subnet_state == {
        "netuid": 1,
        "hotkeys": ["5C4hrfjw9DjXZTzV3MwzrrAr9P1MJhSrvWGWqi1eSuyUpnhM"],
        "coldkeys": ["5C4hrfjw9DjXZTzV3MwzrrAr9P1MJhSrvWGWqi1eSuyUpnhM"],
        "active": [True],
        "validator_permit": [True],
        "pruning_score": [65535],
        "last_update": [0],
        "emission": [0],
        "dividends": [0],
        "incentives": [0],
        "consensus": [0],
        "trust": [0],
        "rank": [0],
        "block_at_registration": [0],
        "alpha_stake": [1000000000],
        "tao_stake": [0],
        "total_stake": [1000000000],
        "emission_history": [[0], [0]],
    }


@pytest.mark.asyncio
async def test_get_subnet_state_not_found(subtensor, mocked_transport):
    mocked_transport.responses["state_call"][
        "SubnetInfoRuntimeApi_get_subnet_state"
    ] = {
        "result": "0x00",
    }

    subnet_state = await subtensor.subnet_info.get_subnet_state(
        netuid=404,
    )

    assert subnet_state is None
