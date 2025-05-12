import typing

if typing.TYPE_CHECKING:
    from ..client import Subtensor


class RuntimeApi:
    def __init__(self, subtensor: "Subtensor"):
        self.subtensor = subtensor
