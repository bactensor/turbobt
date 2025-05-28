import pytest


@pytest.mark.asyncio
async def test_sudo_set_commit_reveal_weights_enabled(subtensor, alice_wallet):
    extrinsic = await subtensor.admin_utils.sudo_set_commit_reveal_weights_enabled(
        netuid=1,
        enabled=True,
        wallet=alice_wallet,
    )

    assert extrinsic.subscription.id == "S6KpbWmhS2jSAsc8"

    subtensor.author.submitAndWatchExtrinsic.assert_called_once_with(
        "AdminUtils",
        "sudo_set_commit_reveal_weights_enabled",
        {
            "netuid": 1,
            "enabled": True,
        },
        key=alice_wallet.coldkey,
    )


@pytest.mark.asyncio
async def test_sudo_set_tempo(subtensor, alice_wallet):
    extrinsic = await subtensor.admin_utils.sudo_set_tempo(
        netuid=1,
        tempo=360,
        wallet=alice_wallet,
    )

    assert extrinsic.subscription.id == "S6KpbWmhS2jSAsc8"

    subtensor.author.submitAndWatchExtrinsic.assert_called_once_with(
        call_module="Sudo",
        call_function="sudo",
        call_args={
            "call": {
                "call_module": "AdminUtils",
                "call_function": "sudo_set_tempo",
                "call_args": {
                    "netuid": 1,
                    "tempo": 360,
                },
            },
        },
        key=alice_wallet.coldkey,
    )


@pytest.mark.asyncio
async def test_sudo_set_weights_set_rate_limit(subtensor, alice_wallet):
    extrinsic = await subtensor.admin_utils.sudo_set_weights_set_rate_limit(
        netuid=1,
        weights_set_rate_limit=100,
        wallet=alice_wallet,
    )

    assert extrinsic.subscription.id == "S6KpbWmhS2jSAsc8"

    subtensor.author.submitAndWatchExtrinsic.assert_called_once_with(
        call_module="Sudo",
        call_function="sudo",
        call_args={
            "call": {
                "call_module": "AdminUtils",
                "call_function": "sudo_set_weights_set_rate_limit",
                "call_args": {
                    "netuid": 1,
                    "weights_set_rate_limit": 100,
                },
            },
        },
        key=alice_wallet.coldkey,
    )
