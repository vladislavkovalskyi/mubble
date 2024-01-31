import typing
from abc import ABC, abstractmethod

from mubble.api import ABCAPI
from mubble.bot.cute_types import BaseCute
from mubble.bot.dispatch.context import Context
from mubble.result import Result

EventT = typing.TypeVar("EventT", bound=BaseCute)
Handler = typing.Callable[typing.Concatenate[EventT, ...], typing.Awaitable[typing.Any]]


class ABCErrorHandler(ABC, typing.Generic[EventT]):
    @abstractmethod
    def catch(self) -> typing.Callable[[typing.Callable], typing.Callable]:
        ...

    @abstractmethod
    async def run(
        self,
        handler: Handler[EventT],
        event: EventT,
        api: ABCAPI,
        ctx: Context,
    ) -> Result[typing.Any, typing.Any]:
        ...


__all__ = ("ABCErrorHandler",)
