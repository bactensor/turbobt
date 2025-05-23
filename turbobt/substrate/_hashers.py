import hashlib
import typing

import xxhash


class Hasher(typing.NamedTuple):
    function: typing.Callable
    hash_length: int


def blake2_128_concat(data: bytearray) -> bytes:
    key = hashlib.blake2b(data, digest_size=16).digest()
    return key + data


def two_x64_concat(data: bytearray) -> bytes:
    key = xxhash.xxh64(data, seed=0).digest()
    return key[::-1] + data


def identity(data: bytearray) -> bytes:
    return data


def xxh128(data: bytearray) -> bytes:
    key1 = xxhash.xxh64(data, seed=0).digest()
    key2 = xxhash.xxh64(data, seed=1).digest()
    return key1[::-1] + key2[::-1]


HASHERS = {
    "Blake2_128Concat": Hasher(blake2_128_concat, 16),
    "Identity": Hasher(identity, 0),
    "Twox64Concat": Hasher(two_x64_concat, 8),
}
