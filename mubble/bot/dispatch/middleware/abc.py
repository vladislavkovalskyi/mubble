import typing
from abc import ABC

from mubble.bot.dispatch.context import Context
from mubble.model import Model

Event = typing.TypeVar("Event", bound=Model)


class ABCMiddleware(ABC, typing.Generic[Event]):
    async def pre(self, event: Event, ctx: Context) -> bool: ...

    async def post(self, event: Event, responses: list[typing.Any], ctx: Context) -> None: ...


__all__ = ("ABCMiddleware",)
