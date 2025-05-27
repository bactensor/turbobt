import typing

import scalecodec

from ._base import Pallet


class Extrinsic(typing.TypedDict):
    extrinsic_hash: str
    extrinsic_length: int
    # call


class Header(typing.TypedDict):
    number: int
    # ...


class Block(typing.TypedDict):
    extrinsics: Extrinsic
    header: Header


class SignedBlock(typing.TypedDict):
    block: Block
    # justifications


class Chain(Pallet):
    async def getBlock(self, block_hash: str | None = None) -> SignedBlock | None:
        """
        Get header and body of a relay chain block.

        :param block_hash: The hash of the block where this transaction was in.
        :type block_hash:
        :return: An object containing information about the requested block.
        :rtype: SignedBlock
        """

        await self.substrate._init_runtime()

        extrinsic_cls = self.substrate._registry.get_decoder_class("Extrinsic")

        result = await self.substrate.rpc(
            method="chain_getBlock",
            params={
                "hash": block_hash,
            },
        )

        if not result:
            return None

        result["block"]["extrinsics"] = [
            extrinsic_cls(
                data=scalecodec.ScaleBytes(extrinsic),
                metadata=self.substrate._metadata,
            ).decode()
            for extrinsic in result["block"]["extrinsics"]
        ]
        result["block"]["header"]["number"] = int(
            result["block"]["header"]["number"],
            16,
        )

        return result

    # TODO accepts list of numbers? Option<ListOrValue<NumberOrHex>>
    async def getBlockHash(self, block_number: int | None = None) -> str | None:
        """
        Get the block hash for a specific block.
        """

        block_hash = await self.substrate.rpc(
            method="chain_getBlockHash",
            params={
                "hash": block_number,
            },
        )

        if not block_hash:
            return None

        return f"0x{block_hash.hex()}"

    async def getHeader(self, block_hash=None) -> Header | None:
        """
        Retrieves the header for a specific block.
        """

        block = await self.substrate.rpc(
            method="chain_getHeader",
            params={
                "hash": block_hash,
            },
        )

        if not block:
            return None

        block["number"] = int(block["number"], 16)

        return block
