import abc
import typing

from fntypes.result import Result

from mubble.api.abc import ABCAPI
from mubble.bot.cute_types import BaseCute
from mubble.bot.rules.adapter.errors import AdapterError
from mubble.model import Model

From = typing.TypeVar("From", bound=Model)
To = typing.TypeVar("To")


class ABCAdapter(abc.ABC, typing.Generic[From, To]):
    @abc.abstractmethod
    async def adapt(self, api: ABCAPI, update: From) -> Result[To, AdapterError]:
        pass


__all__ = ("ABCAdapter",)
