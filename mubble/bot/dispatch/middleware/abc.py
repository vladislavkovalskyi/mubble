import typing
from abc import ABC

from mubble.bot.dispatch.context import Context
from mubble.model import Model
from mubble.types.objects import Update

if typing.TYPE_CHECKING:
    from mubble.bot.rules.adapter.abc import ABCAdapter


class ABCMiddleware[Event: Model](ABC):
    adapter: "ABCAdapter[Update, Event] | None" = None

    async def pre(self, event: Event, ctx: Context) -> bool: ...

    async def post(self, event: Event, responses: list[typing.Any], ctx: Context) -> None: ...


__all__ = ("ABCMiddleware",)
