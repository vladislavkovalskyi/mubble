import asyncio
import dataclasses
import datetime
import typing

from mubble.api import ABCAPI
from mubble.bot.cute_types import BaseCute
from mubble.bot.dispatch.context import Context
from mubble.bot.dispatch.handler.abc import ABCHandler
from mubble.bot.rules.abc import ABCRule
from mubble.model import Model

if typing.TYPE_CHECKING:
    from .machine import Identificator

T = typing.TypeVar("T", bound=Model)
EventModel = typing.TypeVar("EventModel", bound=BaseCute)

Behaviour: typing.TypeAlias = ABCHandler[T] | None


class ShortStateContext(typing.Generic[EventModel], typing.NamedTuple):
    event: EventModel
    context: Context


@dataclasses.dataclass
class ShortState(typing.Generic[EventModel]):
    key: "Identificator"
    ctx_api: ABCAPI
    event: asyncio.Event
    rules: tuple[ABCRule, ...]
    expiration: dataclasses.InitVar[datetime.timedelta | None] = dataclasses.field(
        default=None,
        kw_only=True,
    )
    default_behaviour: Behaviour[EventModel] | None = dataclasses.field(
        default=None, kw_only=True
    )
    on_drop_behaviour: Behaviour[EventModel] | None = dataclasses.field(
        default=None, kw_only=True
    )
    exit_behaviour: Behaviour[EventModel] | None = dataclasses.field(
        default=None, kw_only=True
    )
    expiration_date: datetime.datetime | None = dataclasses.field(
        init=False, kw_only=True
    )
    context: ShortStateContext[EventModel] | None = dataclasses.field(
        default=None, init=False, kw_only=True
    )

    def __post_init__(self, expiration: datetime.timedelta | None = None) -> None:
        self.creation_date = datetime.datetime.now()
        self.expiration_date = (
            (self.creation_date + expiration) if expiration is not None else None
        )

    def cancel(self) -> None:
        """Cancel schedule waiters."""

        waiters = typing.cast(
            typing.Iterable[asyncio.Future[typing.Any]],
            self.event._waiters,
        )
        for future in waiters:
            future.cancel()


__all__ = ("ShortState", "ShortStateContext")
