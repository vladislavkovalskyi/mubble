from abc import ABC, abstractmethod
import typing

if typing.TYPE_CHECKING:
    from mubble.bot.dispatch import Dispatch
    from mubble.api import API


class ABCScenario(ABC):
    @abstractmethod
    def wait(self, api: "API", dispatch: "Dispatch") -> typing.Any:
        pass
