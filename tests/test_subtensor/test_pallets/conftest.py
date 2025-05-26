import pytest_asyncio


@pytest_asyncio.fixture(autouse=True)
def mock_extrinsic(mocked_transport):
    mocked_transport.responses["system_accountNextIndex"] = {
        "result": 1,
    }
    mocked_transport.responses["chain_getBlockHash"] = {
        "result": "0xf0aa135ddac82c7b5ea0de2b021945381bc6a449fdd44386d9956fa0a5ee1e05",
    }
    mocked_transport.responses["author_submitAndWatchExtrinsic"] = {
        "result": "S6KpbWmhS2jSAsc8",
    }
