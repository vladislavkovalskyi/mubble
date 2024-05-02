from mubble.bot.cute_types import MessageCute
from mubble.bot.dispatch.return_manager import MessageReturnManager

from .abc import BaseStateView


class MessageView(BaseStateView[MessageCute]):
    def __init__(self) -> None:
        self.auto_rules = []
        self.handlers = []
        self.middlewares = []
        self.return_manager = MessageReturnManager()

    def get_state_key(self, event: MessageCute) -> int | None:
        return event.chat_id


__all__ = ("MessageView",)
