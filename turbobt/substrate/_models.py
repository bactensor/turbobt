import typing


class Request(typing.NamedTuple):
    """
    JSON-RPC Request.
    """

    method: str
    params: dict | list


class ResponseError(typing.TypedDict):
    """
    JSON-RPC Error Response.
    """

    code: int
    message: str
    data: typing.Any | None


class Response(typing.NamedTuple):
    """
    JSON-RPC Response.
    """

    request: Request
    result: typing.Any | None
    error: ResponseError | None = None


class Subscription:
    # TODO

    def __init__(self, subscription_id, queue):
        self.id = subscription_id
        self.queue = queue

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            item = await self.queue.get()
        # except asyncio.QueueShutDown:
        # TODO
        except Exception as e:
            raise e
            raise StopIteration

        self.queue.task_done()

        if isinstance(item, Exception):
            raise item

        return item
