from __future__ import annotations

import scalecodec.types

from ._base import Pallet


class Utility(Pallet):
    async def batch(
        self,
        calls: list[scalecodec.types.GenericCall],
    ):
        return await self.substrate.rpc(
            method="Utility_batch",
            params={
                "calls": calls,
            },
        )

    async def batch_all(
        self,
        calls: list[scalecodec.types.GenericCall],
    ):
        return await self.substrate.rpc(
            method="Utility_batch_all",
            params={
                "calls": calls,
            },
        )
