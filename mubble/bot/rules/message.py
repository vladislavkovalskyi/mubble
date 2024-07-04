import abc

from mubble.bot.dispatch.context import Context
from mubble.types.objects import Message as MessageEvent

from .abc import ABCRule, Message
from .adapter import EventAdapter


class MessageRule(ABCRule[Message], abc.ABC):
    adapter: EventAdapter[Message] = EventAdapter(MessageEvent, Message)

    @abc.abstractmethod
    async def check(self, message: Message, ctx: Context) -> bool: ...


__all__ = ("MessageRule",)
