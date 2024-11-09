from fntypes.option import Option

from mubble.bot.cute_types import BaseCute
from mubble.bot.dispatch.view import BaseStateView
from mubble.bot.dispatch.waiter_machine.hasher.hasher import ECHO, Hasher
from mubble.tools.functional import from_optional


class StateViewHasher[Event: BaseCute](Hasher[Event, int]):
    view: BaseStateView[Event]

    def __init__(self, view: BaseStateView[Event]) -> None:
        self.view = view
        super().__init__(view.__class__, get_hash_from_data=ECHO)

    def get_data_from_event(self, event: Event) -> Option[int]:
        return from_optional(self.view.get_state_key(event))


__all__ = ("StateViewHasher",)
