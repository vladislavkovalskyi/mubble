import typing
from abc import ABC, abstractmethod

from mubble.bot.cute_types.base import BaseCute

if typing.TYPE_CHECKING:
    from mubble.api import ABCAPI
    from mubble.bot.dispatch.view.abc import ABCStateView

EventT = typing.TypeVar("EventT", bound=BaseCute)


class ABCScenario(ABC, typing.Generic[EventT]):
    @abstractmethod
    def wait(self, api: "ABCAPI", view: "ABCStateView[EventT]") -> typing.Any:
        pass


__all__ = ("ABCScenario",)
