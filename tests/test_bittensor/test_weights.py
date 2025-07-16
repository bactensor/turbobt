import json

import pytest
import pytest_asyncio


@pytest_asyncio.fixture
async def mocked_encrypted_commit(monkeypatch):
    def get_encrypted_commit(
        uids,
        weights,
        version_key,
        tempo,
        current_block,
        netuid,
        subnet_reveal_period_epochs,
        block_time,
    ):
        return (
            json.dumps(
                {
                    "uids": uids,
                    "weights": weights,
                }
            ).encode(),
            123,
        )

    monkeypatch.setattr(
        "bittensor_commit_reveal.get_encrypted_commit",
        get_encrypted_commit,
    )

    yield


@pytest.mark.asyncio
async def test_commit(
    mocked_subtensor, bittensor, alice_wallet, mocked_encrypted_commit
):
    subnet = bittensor.subnet(1)

    await subnet.weights.commit(
        {
            0: 0.2,
            1: 0.8,
        }
    )

    mocked_subtensor.subtensor_module.commit_crv3_weights.assert_awaited_once_with(
        1,
        json.dumps({"uids": [0, 1], "weights": [16384, 65535]}).encode(),
        123,
        wallet=alice_wallet,
    )


@pytest.mark.asyncio
async def test_commit_empty(
    mocked_subtensor, bittensor, alice_wallet, mocked_encrypted_commit
):
    subnet = bittensor.subnet(1)

    await subnet.weights.commit({})

    mocked_subtensor.subtensor_module.commit_crv3_weights.assert_awaited_once_with(
        1,
        json.dumps({"uids": [], "weights": []}).encode(),
        123,
        wallet=alice_wallet,
    )


@pytest.mark.asyncio
async def test_commit_zeros(
    mocked_subtensor, bittensor, alice_wallet, mocked_encrypted_commit
):
    subnet = bittensor.subnet(1)

    await subnet.weights.commit(
        {
            0: 0.0,
            1: 0.0,
        }
    )

    mocked_subtensor.subtensor_module.commit_crv3_weights.assert_awaited_once_with(
        1,
        json.dumps({"uids": [0, 1], "weights": [0, 0]}).encode(),
        123,
        wallet=alice_wallet,
    )
