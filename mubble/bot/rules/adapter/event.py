import typing

from mubble.api.abc import ABCAPI
from mubble.bot.cute_types import BaseCute
from mubble.bot.rules.adapter.abc import ABCAdapter
from mubble.bot.rules.adapter.errors import AdapterError
from mubble.option.option import Nothing
from mubble.result import Error, Ok, Result
from mubble.types.objects import Model, Update

EventT = typing.TypeVar("EventT", bound=Model)
CuteT = typing.TypeVar("CuteT", bound=BaseCute)


class EventAdapter(ABCAdapter[Update, CuteT]):
    def __init__(self, event_name: str, model: type[CuteT]):
        self.event_name = event_name
        self.model = model

    async def adapt(self, api: ABCAPI, update: Update) -> Result[CuteT, AdapterError]:
        update_dct = update.to_dict()
        if self.event_name not in update_dct:
            return Error(
                AdapterError(f"Update is not of event type {self.event_name!r}.")
            )
        if update_dct[self.event_name] is Nothing:
            return Error(AdapterError(f"Update is not an {self.event_name!r}."))
        return Ok(
            self.model.from_update(update_dct[self.event_name].unwrap(), bound_api=api)
        )


__all__ = ("EventAdapter",)
