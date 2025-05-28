import pytest


@pytest.mark.asyncio
async def test_burned_register(subtensor, alice_wallet):
    await subtensor.subtensor_module.burned_register(
        netuid=1,
        hotkey=alice_wallet.hotkey.ss58_address,
        wallet=alice_wallet,
    )

    subtensor.author.submitAndWatchExtrinsic.assert_called_once_with(
        "SubtensorModule",
        "burned_register",
        {
            "netuid": 1,
            "hotkey": "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
        },
        key=alice_wallet.coldkey,
    )


@pytest.mark.asyncio
async def test_commit_crv3_weights(subtensor, alice_wallet):
    await subtensor.subtensor_module.commit_crv3_weights(
        netuid=1,
        commit=b"TEST",
        reveal_round=204,
        wallet=alice_wallet,
    )

    subtensor.author.submitAndWatchExtrinsic.assert_called_once_with(
        "SubtensorModule",
        "commit_crv3_weights",
        {
            "netuid": 1,
            "commit": "0x54455354",
            "reveal_round": 204,
        },
        key=alice_wallet.coldkey,
    )


@pytest.mark.asyncio
async def test_register_network(subtensor, alice_wallet):
    await subtensor.subtensor_module.register_network(
        hotkey=alice_wallet.hotkey.ss58_address,
        mechid=1,
        wallet=alice_wallet,
    )

    subtensor.author.submitAndWatchExtrinsic.assert_called_once_with(
        "SubtensorModule",
        "register_network",
        {
            "hotkey": "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
            "mechid": 1,
        },
        key=alice_wallet.coldkey,
    )


@pytest.mark.asyncio
async def test_serve_axon(subtensor, alice_wallet):
    await subtensor.subtensor_module.serve_axon(
        netuid=1,
        ip="192.168.0.2",
        port=8080,
        wallet=alice_wallet,
        protocol=4,
        version=100,
    )

    subtensor.author.submitAndWatchExtrinsic.assert_called_once_with(
        "SubtensorModule",
        "serve_axon",
        {
            "ip_type": 4,
            "ip": 3232235522,
            "netuid": 1,
            "placeholder1": 0,
            "placeholder2": 0,
            "port": 8080,
            "protocol": 4,
            "version": 100,
        },
        key=alice_wallet.hotkey,
    )


@pytest.mark.asyncio
async def test_serve_axon_tls(subtensor, alice_wallet):
    await subtensor.subtensor_module.serve_axon_tls(
        netuid=1,
        ip="192.168.0.2",
        port=8080,
        certificate=b"CERT",
        wallet=alice_wallet,
        protocol=4,
        version=100,
    )

    subtensor.author.submitAndWatchExtrinsic.assert_called_once_with(
        "SubtensorModule",
        "serve_axon_tls",
        {
            "certificate": b"CERT",
            "ip_type": 4,
            "ip": 3232235522,
            "netuid": 1,
            "placeholder1": 0,
            "placeholder2": 0,
            "port": 8080,
            "protocol": 4,
            "version": 100,
        },
        key=alice_wallet.hotkey,
    )
