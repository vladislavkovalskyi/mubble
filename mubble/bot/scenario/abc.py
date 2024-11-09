import typing
from abc import ABC, abstractmethod

from mubble.bot.cute_types.base import BaseCute

if typing.TYPE_CHECKING:
    from mubble.api import API
    from mubble.bot.dispatch.view.abc import ABCStateView


class ABCScenario[Event: BaseCute](ABC):
    @abstractmethod
    def wait(self, api: "API", view: "ABCStateView[Event]") -> typing.Any:
        pass


__all__ = ("ABCScenario",)
