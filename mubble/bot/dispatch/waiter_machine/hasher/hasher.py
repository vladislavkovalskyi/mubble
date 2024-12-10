import typing
from functools import cached_property

from fntypes.option import Option

from mubble.bot.cute_types import BaseCute
from mubble.bot.dispatch.view.base import BaseView
from mubble.tools.functional import from_optional


def _echo[T](__x: T) -> T:
    return __x


ECHO = _echo


class Hasher[Event: BaseCute, Data]:
    def __init__(
        self,
        view_class: type[BaseView[Event]],
        get_hash_from_data: (
            typing.Callable[[Data], typing.Hashable | None] | None
        ) = None,
        get_data_from_event: typing.Callable[[Event], Data | None] | None = None,
    ) -> None:
        self.view_class = view_class
        self._get_hash_from_data = get_hash_from_data
        self._get_data_from_event = get_data_from_event

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return f"<Hasher {self.name}>"

    @cached_property
    def name(self) -> str:
        return f"{self.view_class.__name__}_{id(self)}"

    def get_hash_from_data(self, data: Data) -> Option[typing.Hashable]:
        if self._get_hash_from_data is None:
            raise NotImplementedError
        return from_optional(self._get_hash_from_data(data))

    def get_data_from_event(self, event: Event) -> Option[Data]:
        if not self._get_data_from_event:
            raise NotImplementedError
        return from_optional(self._get_data_from_event(event))

    def get_hash_from_data_from_event(self, event: Event) -> Option[typing.Hashable]:
        return self.get_data_from_event(event).and_then(self.get_hash_from_data)  # type: ignore


__all__ = ("Hasher",)
