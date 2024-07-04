import typing
from abc import ABC, abstractmethod

from mubble.api.abc import ABCAPI
from mubble.tools.global_context import ABCGlobalContext
from mubble.types import Update


class ABCDispatch(ABC):
    global_context: ABCGlobalContext

    @abstractmethod
    async def feed(self, event: Update, api: ABCAPI) -> bool:
        pass

    @abstractmethod
    def load(self, external: typing.Self) -> None:
        pass


__all__ = ("ABCDispatch",)
