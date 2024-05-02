import typing

from mubble.api.abc import ABCAPI
from mubble.bot.cute_types import MessageCute
from mubble.bot.dispatch.context import Context
from mubble.bot.dispatch.process import check_rule
from mubble.bot.rules.abc import ABCRule
from mubble.modules import logger
from mubble.msgspec_utils import Nothing
from mubble.types.objects import ReplyParameters, Update

from .abc import ABCHandler


class MessageReplyHandler(ABCHandler[MessageCute]):
    def __init__(
        self,
        text: str,
        *rules: ABCRule[MessageCute],
        is_blocking: bool = True,
        as_reply: bool = False,
    ) -> None:
        self.text = text
        self.rules = list(rules)
        self.as_reply = as_reply
        self.is_blocking = is_blocking
        self.preset_context = Context()
    
    def __repr__(self) -> str:
        return "<{}: with rules={!r}, {}: {!r}>".format(
            ("blocking " if self.is_blocking else "")
            + self.__class__.__name__,
            self.rules,
            "answer text as reply" if self.as_reply else "answer text",
            self.text,
        )

    async def check(self, api: ABCAPI, event: Update, ctx: Context | None = None) -> bool:
        ctx = ctx or Context()
        temp_ctx = ctx.copy()
        temp_ctx |= self.preset_context

        for rule in self.rules:
            if not await check_rule(api, rule, event, ctx):
                logger.debug("Rule {!r} failed!", rule)
                return False

        ctx |= temp_ctx
        return True

    async def run(self, event: MessageCute, _: Context) -> typing.Any:
        await event.answer(
            text=self.text,
            reply_parameters=ReplyParameters(event.message_id) if self.as_reply else None,
        )


__all__ = ("MessageReplyHandler",)
