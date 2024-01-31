from mubble.bot.cute_types import CallbackQueryCute
from mubble.bot.dispatch.return_manager import CallbackQueryReturnManager
from mubble.option.option import Some

from .abc import BaseStateView


class CallbackQueryView(BaseStateView[CallbackQueryCute]):
    def __init__(self):
        self.auto_rules = []
        self.handlers = []
        self.middlewares = []
        self.return_manager = CallbackQueryReturnManager()

    def get_state_key(self, event: CallbackQueryCute) -> int | None:
        match event.message:
            case Some(message):
                return message.message_id
            case _:
                return None


__all__ = ("CallbackQueryView",)
