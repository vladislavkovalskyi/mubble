from abc import ABC, abstractmethod
from mubble.api.abc import ABCAPI
from mubble.types import Update
from .view.abc import ABCView
import typing


class ABCDispatch(ABC):
    global_context: dict[str, typing.Any]

    @abstractmethod
    def feed(self, event: Update, api: ABCAPI) -> bool:
        pass

    @abstractmethod
    def load(self, external: "ABCDispatch"):
        pass

    @abstractmethod
    def mount(self, view_t: typing.Type["ABCView"], name: str):
        pass
