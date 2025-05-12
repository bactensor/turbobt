class _ChainErrorMeta(type):
    _exceptions: dict[str, Exception] = {}

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)

        mcs._exceptions.setdefault(cls.__name__, cls)

        return cls

    @classmethod
    def get_exception_class(mcs, exception_name):
        return mcs._exceptions[exception_name]


class SubtensorException(Exception, metaclass=_ChainErrorMeta):
    """Base error for any chain related errors."""

    @classmethod
    def from_error(cls, error):
        try:
            error_cls = _ChainErrorMeta.get_exception_class(
                error["name"],
            )
        except KeyError:
            return cls(error)
        else:
            return error_cls(" ".join(error["docs"]))


# TODO not ChainError
class CustomTransactionError(Exception):
    pass


class StakeAmountTooLow(CustomTransactionError):
    """
    The amount you are staking/unstaking/moving is below the minimum TAO equivalent.
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


# TODO ChainError?
class UnknownBlock(SubtensorException):
    pass


class CommitRevealDisabled(SubtensorException):
    """
    Attemtping to commit/reveal weights when disabled.
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
