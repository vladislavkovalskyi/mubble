from mubble.bot.cute_types.pre_checkout_query import PreCheckoutQueryCute
from mubble.bot.dispatch.return_manager.pre_checkout_query import PreCheckoutQueryManager
from mubble.bot.dispatch.view.base import BaseStateView


class PreCheckoutQueryView(BaseStateView[PreCheckoutQueryCute]):
    def __init__(self) -> None:
        super().__init__()
        self.return_manager = PreCheckoutQueryManager()

    @classmethod
    def get_state_key(cls, event: PreCheckoutQueryCute) -> int | None:
        return event.from_user.id


__all__ = ("PreCheckoutQueryView",)
