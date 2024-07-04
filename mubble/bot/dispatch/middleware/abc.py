import typing
from abc import ABC

from mubble.bot.cute_types.base import BaseCute
from mubble.bot.dispatch.context import Context

T = typing.TypeVar("T", bound=BaseCute)


class ABCMiddleware(ABC, typing.Generic[T]):
    async def pre(self, event: T, ctx: Context) -> bool: ...

    async def post(self, event: T, responses: list[typing.Any], ctx: Context) -> None: ...


__all__ = ("ABCMiddleware",)
