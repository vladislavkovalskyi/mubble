import typing

from mubble.api.abc import ABCAPI
from mubble.bot.cute_types import MessageCute
from mubble.bot.dispatch.context import Context
from mubble.bot.dispatch.process import check_rule
from mubble.bot.rules.abc import ABCRule
from mubble.modules import logger
from mubble.option.option import Nothing
from mubble.types.objects import Update

from .abc import ABCHandler


class MessageReplyHandler(ABCHandler[MessageCute]):
    def __init__(
        self,
        text: str,
        *rules: ABCRule[MessageCute],
        as_reply: bool = False,
        is_blocking: bool = True,
    ):
        self.text = text
        self.rules = list(rules)
        self.as_reply = as_reply
        self.is_blocking = is_blocking
        self.dataclass = MessageCute
        self.ctx = Context()

    async def check(
        self, api: ABCAPI, event: Update, ctx: Context | None = None
    ) -> bool:
        ctx = ctx or Context()
        self.ctx |= ctx
        for rule in self.rules:
            if not await check_rule(api, rule, event, self.ctx):
                logger.debug("Rule {!r} failed!", rule)
                return False
        return True

    async def run(self, event: MessageCute) -> typing.Any:
        await event.answer(
            text=self.text,
            reply_to_message_id=(event.message_id if self.as_reply else Nothing),
        )


__all__ = ("MessageReplyHandler",)
