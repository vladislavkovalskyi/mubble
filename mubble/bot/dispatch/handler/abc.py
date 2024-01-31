import typing
from abc import ABC, abstractmethod

from mubble.api.abc import ABCAPI
from mubble.bot.dispatch.context import Context
from mubble.model import Model
from mubble.types import Update

T = typing.TypeVar("T", bound=Model)


class ABCHandler(ABC, typing.Generic[T]):
    is_blocking: bool
    ctx: Context

    @abstractmethod
    async def run(self, event: T) -> typing.Any:
        pass

    @abstractmethod
    async def check(
        self, api: ABCAPI, event: Update, ctx: Context | None = None
    ) -> bool:
        pass


__all__ = ("ABCHandler",)
