from __future__ import annotations

import typing

from ._base import Pallet
from ._types import StorageValue

if typing.TYPE_CHECKING:
    from ..client import Substrate


class Event(typing.TypedDict):
    """
    Represents a single event in the Substrate system.

    Attributes:
        phase (str): The phase of the event (e.g., "ApplyExtrinsic").
        event (dict): The details of the event, including its module and method.
        topics (list[str]): A list of topics associated with the event.
    """

    phase: str
    event: dict
    topics: list[str]


class System(Pallet):
    def __init__(self, substrate: Substrate):
        self.substrate = substrate

        self.Events = StorageValue[Event](
            substrate,
            "System",
            "Events",
        )

    async def accountNextIndex(self, account_id: str) -> int:
        """
        Retrieve the next account index for the specified account ID from the node.

        This function queries the blockchain node to get the next available
        transaction index (nonce) for the given account. The nonce is used to
        ensure transactions are processed in order and to prevent replay attacks.

        :param account_id: The SS58-encoded address of the account.
        :type account_id: str
        :return: The next account index (nonce) for the specified account.
        :rtype: int
        """

        return await self.substrate.rpc(
            method="system_accountNextIndex",
            params={
                "account": account_id,
            },
        )
