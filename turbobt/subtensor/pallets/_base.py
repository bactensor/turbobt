from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from .. import Subtensor


class Pallet:
    def __init__(self, subtensor: Subtensor):
        self.subtensor = subtensor
