import scalecodec

from ._base import SubstrateRuntime


class Metadata(SubstrateRuntime):
    async def metadata_at_version(
        self,
        version: int,
        block_hash=None,
    ) -> scalecodec.GenericMetadataVersioned | None:
        """
        Get the metadata at the specified version.

        :param version: The version of the metadata
        :type version: int
        :param block_hash: The hash of the block to use for the call.
        :type block_hash: str | None
        :returns: The metadata at the specified version or None if not found.
        :rtype: scalecodec.GenericMetadataVersioned | None
        """

        response = await self.substrate.state.call(
            "Metadata_metadata_at_version",
            f"0x{version.to_bytes(4, byteorder='little').hex()}",
            block_hash,
        )

        metadata15 = self.substrate._registry.create_scale_object(
            "Option<Vec<u8>>",
            data=scalecodec.ScaleBytes(response),
        )
        metadata15.decode()

        if not metadata15.value:
            return None

        metadata15 = self.substrate._registry.create_scale_object(
            "MetadataVersioned",
            data=scalecodec.ScaleBytes(metadata15.value),
        )
        metadata15.decode()

        return metadata15
