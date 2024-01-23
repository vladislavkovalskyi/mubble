import typing
import types
from mubble.bot.rules import ABCRule
from mubble.tools import magic_bundle
from mubble.bot.dispatch.process import check_rule
from mubble.types import Update
from mubble.api.abc import ABCAPI
from .abc import ABCHandler
from mubble.modules import logger

T = typing.TypeVar("T")


class FuncHandler(ABCHandler, typing.Generic[T]):
    def __init__(
        self,
        func: types.FunctionType | typing.Callable,
        rules: list[ABCRule],
        is_blocking: bool = True,
        dataclass: typing.Any | None = dict,
    ):
        self.func = func
        self.is_blocking = is_blocking
        self.rules = rules
        self.dataclass = dataclass
        self.ctx = {}

    async def check(self, api: ABCAPI, event: Update) -> bool:
        self.ctx = {}
        for rule in self.rules:
            if not await check_rule(api, rule, event, self.ctx):
                logger.debug("Rule {} failed", rule)
                return False
        return True

    async def run(self, event: T) -> typing.Any:
        if self.dataclass:
            event = self.dataclass(**event)
        return await self.func(event, **magic_bundle(self.func, self.ctx))
