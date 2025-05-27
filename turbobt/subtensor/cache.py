import asyncio
import collections
import hashlib
import types
import typing

from ..substrate._models import Request, Response
from ..substrate.transports.base import BaseTransport

T = typing.TypeVar("T", bound="CacheTransport")

__all__ = [
    "CacheControl",
    "CacheTransport",
    "InMemoryStorage",
]


class BaseStorage:
    def __len__(self) -> int:
        raise NotImplementedError

    async def get(self, key: str) -> Response | None:
        raise NotImplementedError

    async def set(self, key: str, response: Response) -> None:
        raise NotImplementedError


class InMemoryStorage(BaseStorage):
    def __init__(
        self,
        max_size: int = 128,
    ):
        self.max_size = max_size
        self._cache = collections.OrderedDict[str, Response]()

    def __len__(self):
        return len(self._cache)

    async def get(self, key: str) -> Response | None:
        try:
            self._cache.move_to_end(key, last=False)
        except KeyError:
            return None

        return self._cache[key]

    async def set(self, key: str, response: Response) -> None:
        if len(self._cache) >= self.max_size:
            self._cache.popitem()

        self._cache[key] = response


class CacheResponse(Response):
    pass


class CacheControl:
    def __init__(self):
        pass

    def is_cachable(self, request: Request):
        if request.method == "state_call":
            if isinstance(request.params, dict):
                name = request.params["name"]
            else:
                name = request.params[0]

            if name in (
                "NeuronInfoRuntimeApi_get_neurons_lite",
                "state_getRuntimeVersion",
                "SubnetInfoRuntimeApi_get_dynamic_info",
                "SubnetInfoRuntimeApi_get_subnet_hyperparams",
            ):
                return True

        return False

    def key_generator(self, request: Request) -> str:
        blake2b = hashlib.blake2b(digest_size=16, usedforsecurity=False)
        blake2b.update(request.method.encode())  # ascii?

        if isinstance(request.params, dict):
            params = request.params.values()
        else:
            params = request.params

        for param in params:
            if isinstance(param, str):
                param = param.encode()  # ascii?
            elif param is None:
                param = b""

            blake2b.update(param)  # TODO

        return blake2b.hexdigest()


class CacheTransport(BaseTransport):
    def __init__(
        self,
        transport: BaseTransport,
        cache_control: CacheControl,
        storage: BaseStorage,
    ):
        self._cache_control = cache_control
        self._transport = transport
        self._storage = storage

    async def __aenter__(self: T) -> T:
        await self._transport.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: types.TracebackType | None = None,
    ) -> None:
        await self._transport.__aexit__(exc_type, exc_value, traceback)

    async def send(self, request: Request) -> Response:
        if not self._cache_control.is_cachable(request):
            return await self._transport.send(request)

        key = self._cache_control.key_generator(request)
        cache = await self._storage.get(key)

        if cache:
            return CacheResponse(
                request=request,
                result=cache.result,
            )

        response = await self._transport.send(request)

        if not response.error:
            await self._storage.set(key, response)

        return response

    def subscribe(self, subscription_id) -> asyncio.Queue:
        return self._transport.subscribe(subscription_id)

    def unsubscribe(self, subscription_id) -> asyncio.Queue | None:
        return self._transport.unsubscribe(subscription_id)
