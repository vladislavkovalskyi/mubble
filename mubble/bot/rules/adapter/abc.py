import abc
import typing
from mubble.result import Result
from mubble.bot.rules.adapter.errors import AdapterError
from mubble.api.abc import ABCAPI

UpdateT = typing.TypeVar("UpdateT")
T = typing.TypeVar("T")


class ABCAdapter(abc.ABC, typing.Generic[UpdateT, T]):
    @abc.abstractmethod
    async def adapt(self, api: ABCAPI, update: UpdateT) -> Result[T, AdapterError]:
        pass
