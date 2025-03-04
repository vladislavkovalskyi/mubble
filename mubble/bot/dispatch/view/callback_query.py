from mubble.bot.cute_types.callback_query import CallbackQueryCute
from mubble.bot.dispatch.return_manager.callback_query import CallbackQueryReturnManager
from mubble.bot.dispatch.view.base import BaseStateView


class CallbackQueryView(BaseStateView[CallbackQueryCute]):
    def __init__(self) -> None:
        super().__init__()
        self.return_manager = CallbackQueryReturnManager()

    @classmethod
    def get_state_key(cls, event: CallbackQueryCute) -> int | None:
        return event.message_id.unwrap_or_none()


__all__ = ("CallbackQueryView",)
