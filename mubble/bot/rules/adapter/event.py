from mubble.bot.rules.adapter.abc import ABCAdapter
from mubble.bot.rules.adapter.errors import AdapterError
from mubble.types.objects import Update, Model
from mubble.result import Result, Ok, Error
from mubble.api.abc import ABCAPI
import typing


Event = typing.TypeVar("Event", bound=Model)


class EventAdapter(ABCAdapter[Update, Event]):
    def __init__(self, event_name: str, model: typing.Type[Event]) -> None:
        self.event_name = event_name
        self.model = model

    async def adapt(self, api: ABCAPI, update: Update) -> Result[Event, AdapterError]:
        update_dct = update.to_dict()
        if self.event_name not in update_dct.keys():
            return Error(
                AdapterError(f"Update is not of event type {self.event_name!r}")
            )
        return Ok(self.model(**update_dct[self.event_name].to_dict(), api=api))
