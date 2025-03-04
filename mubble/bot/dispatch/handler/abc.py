import typing
from abc import ABC, abstractmethod

from mubble.api import API
from mubble.bot.dispatch.context import Context
from mubble.tools.adapter.abc import ABCAdapter
from mubble.types.objects import Update


class ABCHandler[Event](ABC):
    final: bool
    adapter: ABCAdapter[Update, Event] | None = None

    @abstractmethod
    async def check(self, api: API, event: Update, ctx: Context | None = None) -> bool:
        pass

    @abstractmethod
    async def run(self, api: API, event: Event, ctx: Context) -> typing.Any:
        pass


__all__ = ("ABCHandler",)
