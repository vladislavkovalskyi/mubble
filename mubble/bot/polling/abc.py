import typing
from abc import ABC, abstractmethod
from mubble.types import Update
from mubble.model import Raw


class ABCPolling(ABC):
    @abstractmethod
    async def get_updates(self) -> list[Raw]:
        pass

    @abstractmethod
    async def listen(self) -> typing.AsyncIterator[list[Update]]:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass
