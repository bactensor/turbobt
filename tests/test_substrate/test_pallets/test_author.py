import pytest


@pytest.mark.asyncio
async def test_submit_and_watch_extrinsic(substrate, mocked_transport, alice_wallet):
    mocked_transport.responses["system_accountNextIndex"] = {
        "result": 1,
    }
    mocked_transport.responses["chain_getBlockHash"] = {
        "result": "0xf0aa135ddac82c7b5ea0de2b021945381bc6a449fdd44386d9956fa0a5ee1e05",
    }
    mocked_transport.responses["author_submitAndWatchExtrinsic"] = {
        "result": "S6KpbWmhS2jSAsc8",
    }

    extrinsic = await substrate.author.submitAndWatchExtrinsic(
        "SubtensorModule",
        "register_network",
        {
            "hotkey": alice_wallet.hotkey.ss58_address,
            "mechid": 1,
        },
        key=alice_wallet.coldkey,
    )

    assert extrinsic.subscription.id == "S6KpbWmhS2jSAsc8"


@pytest.mark.asyncio
async def test_unwatch_extrinsic(substrate, mocked_transport):
    mocked_transport.responses["author_unwatchExtrinsic"] = {
        "result": True,
    }

    result = await substrate.author.unwatchExtrinsic("S6KpbWmhS2jSAsc8")

    assert result is True
