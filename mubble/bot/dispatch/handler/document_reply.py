import typing

from mubble.api.api import API
from mubble.bot.cute_types.message import MessageCute
from mubble.bot.dispatch.context import Context
from mubble.bot.dispatch.handler.base import BaseReplyHandler
from mubble.bot.rules.abc import ABCRule
from mubble.types.objects import InputFile


class DocumentReplyHandler(BaseReplyHandler):
    def __init__(
        self,
        document: InputFile | str,
        *rules: ABCRule,
        caption: str | None = None,
        parse_mode: str | None = None,
        final: bool = True,
        as_reply: bool = False,
        preset_context: Context | None = None,
        **default_params: typing.Any,
    ) -> None:
        self.document = document
        self.parse_mode = parse_mode
        self.caption = caption
        super().__init__(
            *rules,
            final=final,
            as_reply=as_reply,
            preset_context=preset_context,
            **default_params,
        )

    async def run(self, _: API, event: MessageCute, __: Context) -> typing.Any:
        method = event.answer_document if not self.as_reply else event.reply_document
        await method(
            document=self.document,
            parse_mode=self.parse_mode,
            caption=self.caption,
            **self.default_params,
        )


__all__ = ("DocumentReplyHandler",)
