import typing

from mubble.api.api import API
from mubble.bot.cute_types.message import MessageCute
from mubble.bot.dispatch.context import Context
from mubble.bot.dispatch.handler.abc import ABCHandler
from mubble.bot.dispatch.process import check_rule
from mubble.bot.rules.abc import ABCRule
from mubble.modules import logger
from mubble.types.objects import ReplyParameters, Update


class MessageReplyHandler(ABCHandler[MessageCute]):
    def __init__(
        self,
        text: str,
        *rules: ABCRule,
        is_blocking: bool = True,
        as_reply: bool = False,
        preset_context: Context | None = None,
        **default_params: typing.Any,
    ) -> None:
        self.text = text
        self.rules = list(rules)
        self.as_reply = as_reply
        self.is_blocking = is_blocking
        self.default_params = default_params
        self.preset_context = preset_context or Context()

    def __repr__(self) -> str:
        return "<{}: with rules={!r}, {}: {!r}>".format(
            ("blocking " if self.is_blocking else "") + self.__class__.__name__,
            self.rules,
            "answer text as reply" if self.as_reply else "answer text",
            self.text,
        )

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

    async def run(self, _: API, event: MessageCute, __: Context) -> typing.Any:
        await event.answer(
            text=self.text,
            reply_parameters=(
                ReplyParameters(event.message_id) if self.as_reply else None
            ),
            **self.default_params,
        )


__all__ = ("MessageReplyHandler",)
