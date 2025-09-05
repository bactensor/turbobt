from __future__ import annotations

import contextvars
import typing

import scalecodec.types

if typing.TYPE_CHECKING:
    from .client import Bittensor

_batch = contextvars.ContextVar(
    "batch",
    default=None,
)


class Batch:
    def __init__(self, client: Bittensor, force=True):
        self.client = client
        self.force = force
        self.calls = []

    async def __aenter__(self):
        self._token = _batch.set(self)

    async def __aexit__(self, *args, **kwargs):
        _batch.reset(self._token)

        extrinsic = await self.client.subtensor.author.submitAndWatchExtrinsic(
            call_module="Utility",
            call_function="force_batch" if self.force else "batch",
            call_args={"calls": self.calls},
            key=self.client.wallet.coldkey,
        )
        await extrinsic.wait_for_finalization()

    def add(self, call: scalecodec.types.GenericCall):
        self.calls.append(call)


class Transaction(Batch):
    async def __aexit__(self, *args, **kwargs):
        _batch.reset(self._token)

        extrinsic = await self.client.subtensor.author.submitAndWatchExtrinsic(
            call_module="Utility",
            call_function="batch_all",
            call_args={"calls": self.calls},
            key=self.client.wallet.coldkey,
        )
        await extrinsic.wait_for_finalization()


def get_ctx_batch() -> Batch | None:
    return _batch.get()
