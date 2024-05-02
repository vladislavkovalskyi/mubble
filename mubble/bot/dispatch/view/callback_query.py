from fntypes.option import Some

from mubble.bot.cute_types import CallbackQueryCute
from mubble.bot.dispatch.return_manager import CallbackQueryReturnManager

from .abc import BaseStateView


class CallbackQueryView(BaseStateView[CallbackQueryCute]):
    def __init__(self) -> None:
        self.auto_rules = []
        self.handlers = []
        self.middlewares = []
        self.return_manager = CallbackQueryReturnManager()

    def get_state_key(self, event: CallbackQueryCute) -> int | None:
        return event.message.map(lambda variative: variative.v.message_id).unwrap_or_none()


__all__ = ("CallbackQueryView",)
