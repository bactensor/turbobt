from __future__ import annotations

import contextvars
import typing

if typing.TYPE_CHECKING:
    from .client import Bittensor


_block_hash = contextvars.ContextVar(
    "block_hash",
    default=None,
)


def get_ctx_block_hash() -> str | None:
    return _block_hash.get()


class BlockReference:
    def __init__(
        self,
        block_number: int | None = None,
        block_hash: str | None = None,
        *,
        client: Bittensor,
    ):
        self.number = block_number
        self.hash = block_hash
        self.client = client

    async def __aenter__(self):
        if self.hash:
            block_number = self.number
            block_hash = self.hash
        else:
            if self.number is None or self.number == -1:
                block = await self.client.subtensor.chain.getHeader()
                block_number = block["number"]
            else:
                block_number = self.number

            block_hash = await self.client.subtensor.chain.getBlockHash(block_number)

        self._token = _block_hash.set(block_hash)

        return Block(
            block_hash=block_hash,
            block_number=block_number,
            client=self.client,
        )

    async def __aexit__(self, *args, **kwargs):
        _block_hash.reset(self._token)

    async def get(self):
        if self.number is None or self.number == -1:
            block = await self.client.subtensor.chain.getHeader()
            block_number = block["number"]
        else:
            block_number = self.number

        block_hash = await self.client.subtensor.chain.getBlockHash(block_number)

        return Block(
            block_hash=block_hash,
            block_number=block_number,
            client=self.client,
        )

    async def wait(self):
        if self.number is None or self.number == -1:
            return

        await self.client.subtensor.wait_for_block(self.number)


class Block:
    def __init__(
        self,
        block_hash: str,
        block_number: int | None = None,
        *,
        client: Bittensor,
    ):
        self.hash = block_hash
        self.number = block_number
        self.client = client

    async def __aenter__(self):
        self._token = _block_hash.set(self.hash)
        return self

    async def __aexit__(self, *args, **kwargs):
        _block_hash.reset(self._token)


class Blocks:
    def __init__(self, client: Bittensor):
        self.client = client

    def __getitem__(self, key: int | str) -> BlockReference:
        if isinstance(key, int):
            return BlockReference(
                client=self.client,
                block_number=key,
            )

        if isinstance(key, str):
            return BlockReference(
                client=self.client,
                block_hash=key,
            )

        raise TypeError

    async def head(self) -> BlockReference:
        header = await self.client.subtensor.chain.getHeader()

        return BlockReference(
            block_number=header["number"],
            client=self.client,
        )
