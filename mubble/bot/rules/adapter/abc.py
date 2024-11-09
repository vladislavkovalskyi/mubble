import abc
import dataclasses
import typing

from fntypes.result import Result

from mubble.api.api import API
from mubble.bot.dispatch.context import Context
from mubble.bot.rules.adapter.errors import AdapterError
from mubble.model import Model

type AdaptResult[To] = Result[To, AdapterError] | typing.Awaitable[Result[To, AdapterError]]


class ABCAdapter[From: Model, To](abc.ABC):
    ADAPTED_VALUE_KEY: str | None = None

    @abc.abstractmethod
    def adapt(self, api: API, update: From, context: Context) -> AdaptResult[To]:
        pass


@dataclasses.dataclass(slots=True)
class Event[To]:
    obj: To


__all__ = ("ABCAdapter", "AdaptResult", "Event")
