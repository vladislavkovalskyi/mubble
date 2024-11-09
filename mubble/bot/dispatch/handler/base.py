import abc
import typing

from fntypes.result import Result

from mubble.api.api import API
from mubble.api.error import APIError
from mubble.bot.cute_types.message import MessageCute
from mubble.bot.dispatch.context import Context
from mubble.bot.dispatch.handler.abc import ABCHandler
from mubble.bot.dispatch.process import check_rule
from mubble.bot.rules.abc import ABCRule
from mubble.modules import logger
from mubble.types.objects import Update

type APIMethod = typing.Callable[
    typing.Concatenate[MessageCute, ...], typing.Awaitable[Result[typing.Any, APIError]]
]


class BaseReplyHandler(ABCHandler[MessageCute], abc.ABC):
    def __init__(
        self,
        *rules: ABCRule,
        is_blocking: bool = True,
        as_reply: bool = False,
        preset_context: Context | None = None,
        **default_params: typing.Any,
    ) -> None:
        self.rules = list(rules)
        self.as_reply = as_reply
        self.is_blocking = is_blocking
        self.default_params = default_params
        self.preset_context = preset_context or Context()

    def __repr__(self) -> str:
        return f"<{self.__class__.__qualname__}>"

    async def check(self, api: API, event: Update, ctx: Context | None = None) -> bool:
        ctx = Context(raw_update=event) if ctx is None else ctx
        temp_ctx = ctx.copy()
        temp_ctx |= self.preset_context

        for rule in self.rules:
            if not await check_rule(api, rule, event, ctx):
                logger.debug("Rule {!r} failed!", rule)
                return False

        ctx |= temp_ctx
        return True

    @abc.abstractmethod
    async def run(self, api: API, event: MessageCute, ctx: Context) -> typing.Any:
        pass


__all__ = ("BaseReplyHandler",)
