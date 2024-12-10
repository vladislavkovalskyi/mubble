import inspect
import typing

from mubble.bot.dispatch.context import Context
from mubble.tools.adapter.abc import ABCAdapter
from mubble.tools.adapter.raw_update import RawUpdateAdapter
from mubble.types.objects import Update

from .abc import ABCRule, AdaptTo


class FuncRule(ABCRule, typing.Generic[AdaptTo]):
    def __init__(
        self,
        func: typing.Callable[[AdaptTo, Context], typing.Awaitable[bool] | bool],
        adapter: ABCAdapter[Update, AdaptTo] | None = None,
    ) -> None:
        self.func = func
        self.adapter = adapter or RawUpdateAdapter()  # type: ignore

    async def check(self, event: AdaptTo, ctx: Context) -> bool:
        result = self.func(event, ctx)
        if inspect.isawaitable(result):
            result = await result
        return result


__all__ = ("FuncRule",)
