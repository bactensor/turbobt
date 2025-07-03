from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from ..client import Substrate


V = typing.TypeVar("V")


class StorageValue(typing.Generic[V]):
    def __init__(self, substrate: Substrate, module: str, storage: str):
        self.substrate = substrate
        self.module = module
        self.storage = storage

    async def get(self, block_hash=None) -> V:
        return await self.substrate.state.getStorage(
            f"{self.module}.{self.storage}",
            block_hash=block_hash,
        )
