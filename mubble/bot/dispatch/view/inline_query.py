from mubble.bot.cute_types.inline_query import InlineQueryCute
from mubble.bot.dispatch.return_manager import InlineQueryReturnManager
from mubble.bot.dispatch.view.base import BaseStateView


class InlineQueryView(BaseStateView[InlineQueryCute]):
    def __init__(self) -> None:
        super().__init__()
        self.return_manager = InlineQueryReturnManager()

    @classmethod
    def get_state_key(cls, event: InlineQueryCute) -> int | None:
        return event.from_user.id


__all__ = ("InlineQueryView",)
