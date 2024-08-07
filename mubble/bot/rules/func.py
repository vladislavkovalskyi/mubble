import inspect
import typing

from mubble.bot.dispatch.context import Context
from mubble.types.objects import Update

from .abc import ABCAdapter, ABCRule, AdaptTo, RawUpdateAdapter


class FuncRule(ABCRule, typing.Generic[AdaptTo]):
    def __init__(
        self,
        func: typing.Callable[[AdaptTo, Context], typing.Awaitable[bool] | bool],
        adapter: ABCAdapter[Update, AdaptTo] | None = None,
    ):
        self.func = func
        self.adapter = adapter or RawUpdateAdapter()

    async def check(self, event: AdaptTo, ctx: Context) -> bool:
        result = self.func(event, ctx)
        if inspect.isawaitable(result):
            return await result
        return result


__all__ = ("FuncRule",)
