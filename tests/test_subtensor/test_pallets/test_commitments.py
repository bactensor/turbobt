import pytest


@pytest.mark.asyncio
async def test_get_commitment(subtensor, alice_wallet, mocked_transport):
    mocked_transport.responses["state_getStorage"] = {
        "result": "0x000000000000000021010000040500010203",
    }

    netuid = 1

    commitment = await subtensor.commitments.CommitmentOf.get(
        netuid,
        alice_wallet.hotkey.ss58_address,
    )

    assert commitment == {
        "block": 289,
        "deposit": 0,
        "info": {
            "fields": [
                {
                    "Raw4": "0x00010203",
                },
            ],
        },
    }


@pytest.mark.asyncio
async def test_get_commitments(subtensor, alice_wallet, mocked_transport):
    mocked_transport.responses["state_getKeysPaged"] = {
        "result": [
            "0xca407206ec1ab726b2636c4b145ac287419a60ae8b01e6dcaebd7317e43c69bf0200518366b5b1bc7c99d43593c715fdd31c61141abd04a99fd6822c8558854ccde39a5684e7a56da27d",
            "0xca407206ec1ab726b2636c4b145ac2874e7b9012096b41c4eb3aaf947f6ea429",
            "0xca407206ec1ab726b2636c4b145ac287601850e0406400e56fc1672dd2c7ba260200518366b5b1bc7c99d43593c715fdd31c61141abd04a99fd6822c8558854ccde39a5684e7a56da27d",
            "0xca407206ec1ab726b2636c4b145ac287b89891f7701c74220a38fbc5c6b2f548",
            "0xd5e1a2fa16732ce6906189438c0a82c64e7b9012096b41c4eb3aaf947f6ea429",
            "0xd8f314b7f4e6b095f0f8ee4656a448254e7b9012096b41c4eb3aaf947f6ea429",
            "0xf0c365c3cf59d671eb72da0e7a4113c44e7b9012096b41c4eb3aaf947f6ea429",
            "0xf0c365c3cf59d671eb72da0e7a4113c49f1f0515f462cdcf84e0f1d6045dfcbb",
            "0xf35b44951b86069d9273a961f1e3fbeb4e7b9012096b41c4eb3aaf947f6ea429",
        ],
    }
    mocked_transport.responses["state_queryStorageAt"] = {
        "result": [
            {
                "block": "0xe9670fb7fa6fbfd6cad6010501a3b4780f200a9977c802f1eac15bf935cfba48",
                "changes": [
                    [
                        "0xca407206ec1ab726b2636c4b145ac287419a60ae8b01e6dcaebd7317e43c69bf0200518366b5b1bc7c99d43593c715fdd31c61141abd04a99fd6822c8558854ccde39a5684e7a56da27d",
                        "0x000000000000000010010000040500010203",
                    ]
                ],
            },
        ],
    }

    netuid = 2

    commitments = await subtensor.commitments.CommitmentOf.query(
        netuid,
    )

    assert commitments == [
        (
            (
                2,
                "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
            ),
            {
                "deposit": 0,
                "block": 272,
                "info": {
                    "fields": [
                        {
                            "Raw4": "0x00010203",
                        },
                    ],
                },
            },
        ),
    ]


@pytest.mark.asyncio
async def test_set_commitment(subtensor, alice_wallet):
    extrinsic = await subtensor.commitments.set_commitment(
        netuid=1,
        info={
            "fields": [
                [
                    {
                        "Raw4": "0x00010203",
                    },
                ],
            ],
        },
        wallet=alice_wallet,
    )

    assert extrinsic.subscription.id == "S6KpbWmhS2jSAsc8"

    subtensor.author.submitAndWatchExtrinsic.assert_called_once_with(
        "Commitments",
        "set_commitment",
        {
            "netuid": 1,
            "info": {
                "fields": [
                    [
                        {
                            "Raw4": "0x00010203",
                        },
                    ],
                ],
            },
        },
        key=alice_wallet.coldkey,
    )
