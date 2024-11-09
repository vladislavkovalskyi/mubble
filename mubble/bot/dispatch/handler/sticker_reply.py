import typing

from mubble.api.api import API
from mubble.bot.cute_types.message import MessageCute
from mubble.bot.dispatch.context import Context
from mubble.bot.dispatch.handler.base import BaseReplyHandler
from mubble.bot.rules.abc import ABCRule
from mubble.types.objects import InputFile


class StickerReplyHandler(BaseReplyHandler):
    def __init__(
        self,
        sticker: InputFile | str,
        *rules: ABCRule,
        emoji: str | None = None,
        is_blocking: bool = True,
        as_reply: bool = False,
        preset_context: Context | None = None,
        **default_params: typing.Any,
    ) -> None:
        self.sticker = sticker
        self.emoji = emoji
        super().__init__(
            *rules,
            is_blocking=is_blocking,
            as_reply=as_reply,
            preset_context=preset_context,
            **default_params,
        )

    async def run(self, _: API, event: MessageCute, __: Context) -> typing.Any:
        method = event.answer_sticker if not self.as_reply else event.reply_sticker
        await method(sticker=self.sticker, emoji=self.emoji, **self.default_params)


__all__ = ("StickerReplyHandler",)
