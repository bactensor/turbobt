from __future__ import annotations

import typing

import bittensor_wallet

from ...substrate.extrinsic import ExtrinsicResult
from ..types import (
    HotKey,
    NetUid,
)
from ._base import Pallet
from ._types import StorageDoubleMap

if typing.TYPE_CHECKING:
    from .. import Subtensor


class CommitmentInfo(typing.TypedDict):
    fields: list[dict[str, str]]


class Registration(typing.TypedDict):
    block: int
    deposit: int
    info: CommitmentInfo


class Commitments(Pallet):
    def __init__(self, subtensor: Subtensor):
        super().__init__(subtensor)

        self.CommitmentOf = StorageDoubleMap[NetUid, HotKey, Registration](
            subtensor,
            "Commitments",
            "CommitmentOf",
        )

    async def set_commitment(
        self,
        netuid: int,
        info: CommitmentInfo,
        wallet: bittensor_wallet.Wallet,
    ) -> ExtrinsicResult:
        """
        Sets the commitment info for a given hotkey on a subnet.

        :param netuid: The unique identifier of the subnet.
        :type netuid: int
        :param info: The commitment info to set.
        :type info: CommitmentInfo
        :param wallet: The wallet associated with the account making this call.
        :type wallet:
        :return: An asynchronous result of the extrinsic submission.
        :rtype: ExtrinsicResult
        """

        return await self.subtensor.author.submitAndWatchExtrinsic(
            "Commitments",
            "set_commitment",
            {
                "netuid": netuid,
                "info": info,
            },
            key=wallet.coldkey,
        )
