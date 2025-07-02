from __future__ import annotations

import datetime
import typing

from ._base import Pallet
from ._types import StorageValue

if typing.TYPE_CHECKING:
    from ..client import Substrate


class Timestamp(Pallet):
    def __init__(self, substrate: Substrate):
        self.substrate = substrate

        self.Now = StorageValue[datetime.datetime](
            substrate,
            "Timestamp",
            "Now",
        )
