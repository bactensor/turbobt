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


@pytest.mark.asyncio
async def test_evm_addresses_fetch(subtensor, mocked_transport):
    mocked_transport.responses["state_getKeysPaged"] = {
        "result": [
            "0x658faa385070e074c85bf6b568cf05552ee3ea5cc28fb0bcd7e9c900544e35b24b9bd30d03d0266b0c00a71a89063ba6541ca300",
            "0x658faa385070e074c85bf6b568cf05552ee3ea5cc28fb0bcd7e9c900544e35b24b9bd30d03d0266b0c00ce2b3c8f6925c6c8c500",
            "0x658faa385070e074c85bf6b568cf05552ee3ea5cc28fb0bcd7e9c900544e35b24b9bd30d03d0266b0c00d149990e23eec1414200",
        ],
    }
    mocked_transport.responses["state_queryStorageAt"] = {
        "result": [
            {
                "block": "0x388b5c4daa4e254119cb1a62b061af72b4d562977a5ac7d698e79698da4ffaa2",
                "changes": [
                    [
                        "0x658faa385070e074c85bf6b568cf05552ee3ea5cc28fb0bcd7e9c900544e35b24b9bd30d03d0266b0c00a71a89063ba6541ca300",
                        "0x77407f1709d339f5583feac922c0592e248f785f507e560000000000",
                    ],
                    [
                        "0x658faa385070e074c85bf6b568cf05552ee3ea5cc28fb0bcd7e9c900544e35b24b9bd30d03d0266b0c00ce2b3c8f6925c6c8c500",
                        "0xa873b6e2ed71bae54f232fb622b713239f0ec54cc87e530000000000",
                    ],
                    [
                        "0x658faa385070e074c85bf6b568cf05552ee3ea5cc28fb0bcd7e9c900544e35b24b9bd30d03d0266b0c00d149990e23eec1414200",
                        "0xba6a023c87dd55a0b862925278e77056677e92b7f37e530000000000",
                    ],
                ],
            },
        ],
    }

    evm_addresses = await subtensor.subtensor_module.AssociatedEvmAddress.query(12)

    assert evm_addresses == [
        ((12, 163), ("0x77407f1709d339f5583feac922c0592e248f785f", 5668432)),
        ((12, 197), ("0xa873b6e2ed71bae54f232fb622b713239f0ec54c", 5471944)),
        ((12, 66), ("0xba6a023c87dd55a0b862925278e77056677e92b7", 5471987)),
    ]
