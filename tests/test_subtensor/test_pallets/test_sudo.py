import pytest


@pytest.mark.asyncio
async def test_sudo(subtensor, alice_wallet):
    extrinsic = await subtensor.sudo.sudo(
        "AdminUtils",
        "sudo_set_tempo",
        {
            "netuid": 1,
            "tempo": 360,
        },
        era=None,
        wallet=alice_wallet,
    )

    assert extrinsic.subscription.id == "0x53364b7062576d6853326a5341736338"

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
        era=None,
        key=alice_wallet.coldkey,
    )
