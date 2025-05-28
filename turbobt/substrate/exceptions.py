class ChainErrorMeta(type):
    _exceptions: dict[str, Exception] = {}

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)

        mcs._exceptions.setdefault(cls.__name__, cls)

        return cls

    @classmethod
    def get_exception_class(mcs, exception_name):
        return mcs._exceptions[exception_name]


class SubstrateException(Exception):
    """Base error for any chain related errors."""

    @classmethod
    def from_error(cls, error):
        try:
            error_cls = ChainErrorMeta.get_exception_class(
                error["name"],
            )
        except KeyError:
            return cls(error)
        else:
            return error_cls(" ".join(error["docs"]))


class UnknownBlock(SubstrateException):
    pass


class CustomTransactionError(SubstrateException):
    pass
