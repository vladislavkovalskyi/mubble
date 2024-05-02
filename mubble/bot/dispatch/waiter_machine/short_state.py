import asyncio
import dataclasses
import datetime
import typing

from mubble.api import ABCAPI
from mubble.bot.cute_types import BaseCute
from mubble.bot.dispatch.handler.abc import ABCHandler
from mubble.bot.rules.abc import ABCRule

if typing.TYPE_CHECKING:
    from .machine import Identificator

EventModel = typing.TypeVar("EventModel", bound=BaseCute)
Behaviour: typing.TypeAlias = ABCHandler | None


@dataclasses.dataclass
class ShortState(typing.Generic[EventModel]):
    key: "Identificator"
    ctx_api: ABCAPI
    event: asyncio.Event
    rules: tuple[ABCRule[EventModel], ...]
    _: dataclasses.KW_ONLY
    expiration: dataclasses.InitVar[datetime.timedelta | None] = dataclasses.field(default=None)
    default_behaviour: Behaviour | None = dataclasses.field(default=None)
    on_drop_behaviour: Behaviour | None = dataclasses.field(default=None)
    expiration_date: datetime.datetime | None = dataclasses.field(init=False)

    def __post_init__(self, expiration: datetime.timedelta | None = None) -> None:
        self.expiration_date = (
            datetime.datetime.now() - expiration
        ) if expiration is not None else None


__all__ = ("ShortState",)
