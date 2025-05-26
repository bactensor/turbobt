import pytest


@pytest.mark.asyncio
async def test_get_header(substrate, mocked_transport):
    mocked_transport.responses["chain_getHeader"] = {
        "result": {
            "parentHash": "0x2bb80cc429296b4da191bcec87d4b526ca0e407b4756f2a387a87d3b8e26ae42",
            "number": "0xf54",
            "stateRoot": "0xfb9e07dd769d95a30ab04e1e801b1400df1261487cddab93dc64628ad95cec56",
            "extrinsicsRoot": "0xe5b4ae1cda6591fa8a8026bef64c5d712f7dc6c0dc700f74d1670139e55c220d",
            "digest": {
                "logs": [
                    "0x066175726120c65dd0a001000000",
                    "0x0466726f6e88016cf22a0277ba8ff8e59961a06a8d069319b70310036243621a257f53a12c1c2700",
                    "0x0561757261010106b919906a40cc0db25fb60404f5323902641f4696b0a83b8f0b5d08a1ccb3303d2153015f0451901bcf50867bf182d991876176c8ccc9bf55aed1748085ac8d",
                ]
            },
        },
    }

    block_header = await substrate.chain.getHeader()

    assert block_header == {
        "parentHash": "0x2bb80cc429296b4da191bcec87d4b526ca0e407b4756f2a387a87d3b8e26ae42",
        "number": 3924,
        "stateRoot": "0xfb9e07dd769d95a30ab04e1e801b1400df1261487cddab93dc64628ad95cec56",
        "extrinsicsRoot": "0xe5b4ae1cda6591fa8a8026bef64c5d712f7dc6c0dc700f74d1670139e55c220d",
        "digest": {
            "logs": [
                "0x066175726120c65dd0a001000000",
                "0x0466726f6e88016cf22a0277ba8ff8e59961a06a8d069319b70310036243621a257f53a12c1c2700",
                "0x0561757261010106b919906a40cc0db25fb60404f5323902641f4696b0a83b8f0b5d08a1ccb3303d2153015f0451901bcf50867bf182d991876176c8ccc9bf55aed1748085ac8d",
            ]
        },
    }


@pytest.mark.asyncio
async def test_get_header_does_not_exist(substrate, mocked_transport):
    mocked_transport.responses["chain_getHeader"] = {
        "result": None,
    }

    block_header = await substrate.chain.getHeader(
        "0x3fe8c77075d8194ed0bb7fd70d7b8cc91c12826c7f04df9f04c4235f0f6a966c"
    )

    assert block_header is None


@pytest.mark.asyncio
async def test_get_block(substrate, mocked_transport):
    mocked_transport.responses["chain_getBlock"] = {
        "result": {
            "block": {
                "header": {
                    "parentHash": "0x3fe8c77075d8194ed0bb7fd70d7b8cc91c12826c7f04df9f04c4235f0f6a966b",
                    "number": "0x3a6",
                    "stateRoot": "0x7e08c53c205b2d7766884935e96dab4cdd11e7055024603b42023894bec3c33d",
                    "extrinsicsRoot": "0x937ca90d15a79bf046edeb94a02ccc65de71b7985e9bb215d5e31bd5fea3b962",
                    "digest": {
                        "logs": [
                            "0x066175726120694fd0a001000000",
                            "0x0466726f6e88010b5bab658f24b6f14179a5d50e59a7901785c97358ebcd910a8186ba6ba79f9800",
                            "0x05617572610101f6a1e1e554fd7a9bc6adaf7fdbab553771bdc8ce354c95c38ce03c76d130797de48a244d8dc06d1c9c84ba82b02ed0dcc1dd3e88fd4e10271003cb402c1bbc8f",
                        ]
                    },
                },
                "extrinsics": ["0x280402000b8a8c6d0b9701"],
            },
            "justifications": None,
        }
    }

    block = await substrate.chain.getBlock()

    assert block == {
        "block": {
            "header": {
                "parentHash": "0x3fe8c77075d8194ed0bb7fd70d7b8cc91c12826c7f04df9f04c4235f0f6a966b",
                "number": 934,
                "stateRoot": "0x7e08c53c205b2d7766884935e96dab4cdd11e7055024603b42023894bec3c33d",
                "extrinsicsRoot": "0x937ca90d15a79bf046edeb94a02ccc65de71b7985e9bb215d5e31bd5fea3b962",
                "digest": {
                    "logs": [
                        "0x066175726120694fd0a001000000",
                        "0x0466726f6e88010b5bab658f24b6f14179a5d50e59a7901785c97358ebcd910a8186ba6ba79f9800",
                        "0x05617572610101f6a1e1e554fd7a9bc6adaf7fdbab553771bdc8ce354c95c38ce03c76d130797de48a244d8dc06d1c9c84ba82b02ed0dcc1dd3e88fd4e10271003cb402c1bbc8f",
                    ]
                },
            },
            "extrinsics": [
                {
                    "extrinsic_hash": "0xb905206696a6d4307da80c3686715c6ee7a25e02dc9e63352fe8b8557e04ff7d",
                    "extrinsic_length": 10,
                    "call": {
                        "call_index": "0x0200",
                        "call_function": "set",
                        "call_module": "Timestamp",
                        "call_args": [
                            {"name": "now", "type": "Moment", "value": 1748243418250}
                        ],
                        "call_hash": "0x188196e4d4204e99898e9df7130e2b9e62e6bfb6d2143dd1349c629f33671613",
                    },
                }
            ],
        },
        "justifications": None,
    }


@pytest.mark.asyncio
async def test_get_block_does_not_exist(substrate, mocked_transport):
    mocked_transport.responses["chain_getBlock"] = {
        "result": None,
    }

    block = await substrate.chain.getBlock(
        "0x3fe8c77075d8194ed0bb7fd70d7b8cc91c12826c7f04df9f04c4235f0f6a966b"
    )

    assert block is None


@pytest.mark.asyncio
async def test_get_block_hash(substrate, mocked_transport):
    mocked_transport.responses["chain_getBlockHash"] = {
        "result": "0x5fafc9ff0d69341e3eb0e8721fa5641f8d6aae5c7eaee0549a4531818c1cda0c",
    }

    block_hash = await substrate.chain.getBlockHash(1)

    assert (
        block_hash
        == "0x5fafc9ff0d69341e3eb0e8721fa5641f8d6aae5c7eaee0549a4531818c1cda0c"
    )


@pytest.mark.asyncio
async def test_get_block_hash_does_not_exist(substrate, mocked_transport):
    mocked_transport.responses["chain_getBlockHash"] = {
        "result": None,
    }

    block_hash = await substrate.chain.getBlockHash(404)

    assert block_hash is None
