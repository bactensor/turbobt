from __future__ import annotations

import typing

import scalecodec

from ...substrate._hashers import HASHERS
from ..types import HotKey

if typing.TYPE_CHECKING:
    from ...subtensor import Subtensor


K1 = typing.TypeVar("K1")
K2 = typing.TypeVar("K2")
V = typing.TypeVar("V")


class StorageDoubleMap(typing.Generic[K1, K2, V]):
    def __init__(self, subtensor: Subtensor, module: str, storage: str):
        self.subtensor = subtensor
        self.module = module
        self.storage = storage

    async def get(self, key1: K1, key2: K2, block_hash=None) -> V:
        return await self.subtensor.state.getStorage(
            f"{self.module}.{self.storage}",
            key1,
            key2,
            block_hash=block_hash,
        )

    async def query(
        self,
        *args,
        count: int = 100,
        start_key: str = "",
        block_hash: str = None,
    ):
        keys = await self.subtensor.state.getKeysPaged(
            f"{self.module}.{self.storage}",
            *args,
            block_hash=block_hash,
            count=count,
            start_key=start_key,
        )
        results = await self.subtensor.state.queryStorageAt(
            keys,
            block_hash=block_hash,
        )

        pallet = self.subtensor._metadata.get_metadata_pallet(self.module)
        storage_function = pallet.get_storage_function(self.storage)

        prefix = self.subtensor.state._storage_key(
            pallet,
            storage_function,
            args,
        )

        param_types = storage_function.get_params_type_string()
        param_hashers = storage_function.get_param_hashers()

        key_type_string = []
        for n in range(len(args), len(param_types)):
            try:
                hasher = HASHERS[param_hashers[n]]
            except KeyError:
                raise NotImplementedError(param_hashers[n])

            key_type_string.append(
                f"[u8; {hasher.hash_length}]"
            )
            key_type_string.append(param_types[n])

        key_type = self.subtensor._registry.create_scale_object(
            f"({', '.join(key_type_string)})",
        )
        value_type = self.subtensor._registry.create_scale_object(
            storage_function.get_value_type_string(),
        )

        results = (
            (
                bytearray.fromhex(key.removeprefix(prefix)),
                bytearray.fromhex(value[2:]),
            )
            for result in results
            for key, value in result["changes"]
            if key.startswith(prefix)   # TODO?
        )
        results = (
            (
                key_type.decode(
                    scalecodec.ScaleBytes(key),
                ),
                value_type.decode(
                    scalecodec.ScaleBytes(value),
                ),
            )
            for key, value in results
            if key  # TODO but has a value???
        )
        results = (
            (
                key[-1],    # TODO depends on number of args
                value,
            )
            for key, value in results
        )

        if self.__orig_class__.__args__[1] is HotKey:
            results = (
                (
                    scalecodec.utils.ss58.ss58_encode(key),
                    value,
                )
                for key, value in results
            )

        return list(results)
