from __future__ import annotations

import typing

import scalecodec

from ...substrate._hashers import HASHERS
from ...substrate._models import Subscription
from ...substrate.pallets.state import StorageChangeSet

if typing.TYPE_CHECKING:
    from ..client import Substrate


V = typing.TypeVar("V")


class StorageSubscription:
    def __init__(self, subscription: Subscription, decode: typing.Callable):
        self._subscription = subscription
        self._decode = decode

    @property
    def id(self):
        return self._subscription.id

    def __aiter__(self):
        return self

    async def __anext__(self):
        return self._decode(await self._subscription.__anext__())


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

    async def subscribe(self):
        subscription_id = await self.substrate.state.subscribeStorage(
            f"{self.module}.{self.storage}",
        )

        return StorageSubscription(
            await self.substrate.subscribe(subscription_id),
            self._decode,
        )

    def _decode(
        self,
        storage_change_set: StorageChangeSet,
    ) -> list[tuple[tuple, V]]:
        pallet = self.substrate._metadata.get_metadata_pallet(self.module)
        storage_function = pallet.get_storage_function(self.storage)

        param_types = storage_function.get_params_type_string()
        param_hashers = storage_function.get_param_hashers()

        key_type_string = []

        for param_hasher, param_type in zip(param_hashers, param_types):
            try:
                hasher = HASHERS[param_hasher]
            except KeyError:
                raise NotImplementedError(param_hasher)

            key_type_string.append(f"[u8; {hasher.hash_length}]")
            key_type_string.append(param_type)

        key_type = self.substrate._registry.create_scale_object(
            f"({', '.join(key_type_string)})",
        )
        value_type = self.substrate._registry.create_scale_object(
            storage_function.get_value_type_string(),
        )

        prefix = self.substrate.state._storage_key(
            pallet,
            storage_function,
            [],
        )

        changes = (
            (
                bytearray.fromhex(key.removeprefix(prefix)),
                bytearray.fromhex(value[2:]),
            )
            for key, value in storage_change_set["changes"]
        )
        changes = (
            (
                key_type.decode(
                    scalecodec.ScaleBytes(key),
                ),
                value_type.decode(
                    scalecodec.ScaleBytes(value),
                ),
            )
            for key, value in changes
        )

        storage_change_set["changes"] = list(changes)

        return storage_change_set
