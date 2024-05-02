import abc
import typing

from fntypes.result import Result

from mubble.api.abc import ABCAPI
from mubble.bot.cute_types import BaseCute
from mubble.bot.rules.adapter.errors import AdapterError
from mubble.model import Model

UpdateT = typing.TypeVar("UpdateT", bound=Model)
CuteT = typing.TypeVar("CuteT", bound=BaseCute)


class ABCAdapter(abc.ABC, typing.Generic[UpdateT, CuteT]):
    @abc.abstractmethod
    async def adapt(self, api: ABCAPI, update: UpdateT) -> Result[CuteT, AdapterError]:
        pass


__all__ = ("ABCAdapter",)
