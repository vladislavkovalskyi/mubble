from mubble.bot.dispatch.context import Context
from mubble.types.enums import MessageEntityType

from .text import Message, TextMessageRule


class HasMention(TextMessageRule):
    async def check(self, message: Message, ctx: Context) -> bool:
        if not message.entities.unwrap_or_none():
            return False
        return any(entity.type == MessageEntityType.MENTION for entity in message.entities.unwrap())


__all__ = ("HasMention",)
