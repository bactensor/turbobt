from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from ..client import Substrate


class Pallet:
    def __init__(self, substrate: Substrate):
        self.substrate = substrate
