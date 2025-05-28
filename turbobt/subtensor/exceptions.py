from turbobt.substrate.exceptions import (
    ChainErrorMeta,
    SubstrateException,
)


class SubtensorException(SubstrateException, metaclass=ChainErrorMeta):
    """
    Base error for any Subtensor related errors.
    """


class ColdkeyInSwapSchedule(SubtensorException):
    """
    Your coldkey is set to be swapped. No transfer operations are possible.
    """


class StakeAmountTooLow(SubtensorException):
    """
    The amount you are staking/unstaking/moving is below the minimum TAO equivalent.
    """


class BalanceTooLow(SubtensorException):
    """
    The amount of stake you have is less than you have requested.
    """


class SubnetDoesntExist(SubtensorException):
    """
    This subnet does not exist.
    """


class HotkeyAccountDoesntExist(SubtensorException):
    """
    Hotkey is not registered on Bittensor network.
    """


class NotEnoughStakeToWithdraw(SubtensorException):
    """
    You do not have enough TAO equivalent stake to remove/move/transfer, including the unstake fee.
    """


class RateLimitExceeded(SubtensorException):
    """
    Too many transactions submitted (other than Axon serve/publish extrinsic).
    """


class InsufficientLiquidity(SubtensorException):
    """
    The subnet's pool does not have sufficient liquidity for this transaction.
    """


class SlippageTooHigh(SubtensorException):
    """
    The slippage exceeds your limit. Try reducing the transaction amount.
    """


class TransferDisallowed(SubtensorException):
    """
    This subnet does not allow stake transfer.
    """


class HotKeyNotRegisteredInNetwork(SubtensorException):
    """
    The hotkey is not registered in the selected subnet.
    """


class InvalidIpAddress(SubtensorException):
    """
    Axon connection info cannot be parsed into a valid IP address.
    """


class ServingRateLimitExceeded(SubtensorException):
    """
    Rate limit exceeded for axon serve/publish extrinsic.
    """


class InvalidPort(SubtensorException):
    """
    Axon connection info cannot be parsed into a valid port.
    """


class BadRequest(SubtensorException):
    """
    Unclassified error.
    """


class NetworkTxRateLimitExceeded(SubtensorException):
    """
    A transactor exceeded the rate limit for add network transaction.
    """


class NotEnoughBalanceToStake(SubtensorException):
    """
    The caller is requesting adding more stake than there exists in the coldkey account.
    See: "[add_stake()]"
    """


class CommitRevealDisabled(SubtensorException):
    """
    Attempting to commit/reveal weights when disabled.
    """


class CommittingWeightsTooFast(SubtensorException):
    """
    A transactor exceeded the rate limit for setting weights.
    """


class CommitmentSetRateLimitExceeded(SubtensorException):
    """
    Account is trying to commit data too fast, rate limit exceeded.
    """


class HotKeyAlreadyRegisteredInSubNet(SubtensorException):
    """
    The caller is requesting registering a neuron which already exists in the active set.
    """


# # https://github.com/opentensor/subtensor/blob/main/pallets/subtensor/src/lib.rs#L1700-L1714
SUBSTRATE_CUSTOM_ERRORS = {
    "Custom error: 0": ColdkeyInSwapSchedule,
    "Custom error: 1": StakeAmountTooLow,
    "Custom error: 2": BalanceTooLow,
    "Custom error: 3": SubnetDoesntExist,
    "Custom error: 4": HotkeyAccountDoesntExist,
    "Custom error: 5": NotEnoughStakeToWithdraw,
    "Custom error: 6": RateLimitExceeded,
    "Custom error: 7": InsufficientLiquidity,
    "Custom error: 8": SlippageTooHigh,
    "Custom error: 9": TransferDisallowed,
    "Custom error: 10": HotKeyNotRegisteredInNetwork,
    "Custom error: 11": InvalidIpAddress,
    "Custom error: 12": ServingRateLimitExceeded,
    "Custom error: 13": InvalidPort,
    "Custom error: 255": BadRequest,
}
