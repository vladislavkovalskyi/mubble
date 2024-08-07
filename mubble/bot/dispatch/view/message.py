import typing

from mubble.bot.cute_types import MessageCute
from mubble.bot.dispatch.return_manager import MessageReturnManager
from mubble.types import Update, UpdateType

from .abc import BaseStateView

MessageUpdateType: typing.TypeAlias = typing.Literal[
    UpdateType.MESSAGE,
    UpdateType.BUSINESS_MESSAGE,
    UpdateType.CHANNEL_POST,
    UpdateType.EDITED_BUSINESS_MESSAGE,
    UpdateType.EDITED_CHANNEL_POST,
    UpdateType.EDITED_MESSAGE,
]


class MessageView(BaseStateView[MessageCute]):
    def __init__(self, *, update_type: MessageUpdateType | None = None) -> None:
        self.auto_rules = []
        self.handlers = []
        self.update_type = update_type
        self.middlewares = []
        self.return_manager = MessageReturnManager()

    def __repr__(self) -> str:
        return "<{}: {!r}>".format(
            self.__class__.__name__,
            "any message update" if self.update_type is None else self.update_type.value,
        )

    def get_state_key(self, event: MessageCute) -> int | None:
        return event.chat_id

    async def check(self, event: Update) -> bool:
        if not await super().check(event):
            return False
        return True if self.update_type is None else self.update_type == event.update_type


__all__ = ("MessageView",)
