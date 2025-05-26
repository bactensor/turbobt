from __future__ import annotations

import asyncio
import typing

import scalecodec.types

from ._models import Subscription
from .exceptions import SubstrateException

if typing.TYPE_CHECKING:
    from .client import Substrate


class ExtrinsicResult:
    """
    Asynchronous Extrinsic Result.
    """

    def __init__(
        self,
        extrinsic: scalecodec.types.GenericExtrinsic,
        subscription: Subscription,
        substrate: Substrate,
    ):
        self.extrinsic = extrinsic
        self.subscription = subscription
        self.substrate = substrate

    async def wait_for_inclusion(self):
        async for status in self.subscription:
            if "inBlock" not in status:
                continue

            asyncio.create_task(
                self.substrate.author.unwatchExtrinsic(
                    self.subscription.id,
                )
            )

            return

    async def wait_for_finalization(self):
        async for status in self.subscription:
            if "finalized" not in status:
                continue

            asyncio.create_task(
                self.substrate.author.unwatchExtrinsic(
                    self.subscription.id,
                )
            )

            block, events = await asyncio.gather(
                self.substrate.chain.getBlock(status["finalized"]),
                self.substrate.state.getStorage(
                    "System.Events",
                    block_hash=status["finalized"],
                ),
            )

            extrinsic_hash = f"0x{self.extrinsic.extrinsic_hash.hex()}"
            extrinsic_idx = next(
                i
                for i, extrinsic in enumerate(block["block"]["extrinsics"])
                if extrinsic["extrinsic_hash"] == extrinsic_hash
            )

            events = [
                event for event in events if event["extrinsic_idx"] == extrinsic_idx
            ]

            try:
                extrinsic_failed = next(
                    event
                    for event in events
                    if event["module_id"] == "System"
                    and event["event_id"] == "ExtrinsicFailed"
                )
            except StopIteration:
                return

            dispatch_error = extrinsic_failed["event"]["attributes"]["dispatch_error"]

            if "Module" in dispatch_error:
                module_error = self.substrate._metadata.get_module_error(
                    module_index=dispatch_error["Module"]["index"],
                    error_index=int.from_bytes(
                        bytes.fromhex(dispatch_error["Module"]["error"][2:]),
                        byteorder="little",
                    ),
                )

                raise SubstrateException.from_error(module_error.value)

            raise SubstrateException(dispatch_error)
