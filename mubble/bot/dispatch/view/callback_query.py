from mubble.bot.cute_types.callback_query import CallbackQueryCute
from mubble.bot.dispatch.return_manager.callback_query import CallbackQueryReturnManager
from mubble.bot.dispatch.view.base import BaseStateView


class CallbackQueryView(BaseStateView[CallbackQueryCute]):
    def __init__(self) -> None:
        self.auto_rules = []
        self.handlers = []
        self.middlewares = []
        self.return_manager = CallbackQueryReturnManager()

    def get_state_key(self, event: CallbackQueryCute) -> int | None:
        return event.message_id.unwrap_or_none()


__all__ = ("CallbackQueryView",)
