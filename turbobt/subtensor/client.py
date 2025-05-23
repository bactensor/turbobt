import scalecodec

from ..substrate.client import Substrate
from .cache import (
    CacheControl,
    CacheTransport,
    InMemoryStorage,
)
from .pallets import (
    AdminUtils,
    Commitments,
    SubtensorModule,
    Sudo,
)
from .runtime import (
    NeuronInfoRuntimeApi,
    SubnetInfoRuntimeApi,
)


class Subtensor(Substrate):
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        """
        Initialize a Subtensor instance.
        See Substrate.__init__ for more details.
        """

        super().__init__(*args, **kwargs)

        self.admin_utils = AdminUtils(self)
        self.commitments = Commitments(self)
        self.subtensor_module = SubtensorModule(self)
        self.sudo = Sudo(self)

        self.neuron_info = NeuronInfoRuntimeApi(self)
        self.subnet_info = SubnetInfoRuntimeApi(self)

    async def api_call(self, api, method, block_hash=None, **kwargs):
        await self._init_runtime()

        # XXX
        api = self._registry.type_registry["apis"][api]
        method = api["methods"][method]
        data = bytearray()

        for param in method["inputs"]:
            scale = self._registry.create_scale_object(f"scale_info::{param['type']}")
            scale.encode(kwargs[param["name"]])

            data.extend(scale.data.data)

        response = await self.state.call(
            f"{api['name']}_{method['name']}",
            data.hex(),
            block_hash,
        )

        if not isinstance(response, bytearray):
            return response

        output = self._registry.create_scale_object(f"scale_info::{method['output']}")

        return output.decode(
            scalecodec.ScaleBytes(response),
        )


class CacheSubtensor(Subtensor):
    def _init_transport(self, *args, **kwargs):
        transport = super()._init_transport(*args, **kwargs)

        return CacheTransport(
            transport=transport,
            cache_control=CacheControl(),
            storage=InMemoryStorage(),
        )
