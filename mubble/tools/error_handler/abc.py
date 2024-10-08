import typing
from abc import ABC, abstractmethod

from fntypes.result import Result

from mubble.api import API
from mubble.bot.dispatch.context import Context

EventT = typing.TypeVar("EventT")
Handler = typing.Callable[typing.Concatenate[EventT, ...], typing.Awaitable[typing.Any]]


class ABCErrorHandler(ABC, typing.Generic[EventT]):
    @abstractmethod
    def __call__(
        self,
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> typing.Callable[
        [typing.Callable[..., typing.Any]], typing.Callable[..., typing.Any]
    ]:
        """Decorator for registering callback as an error handler."""

    @abstractmethod
    async def run(
        self,
        handler: Handler[EventT],
        event: EventT,
        api: API,
        ctx: Context,
    ) -> Result[typing.Any, typing.Any]:
        """Run error handler."""


__all__ = ("ABCErrorHandler",)
