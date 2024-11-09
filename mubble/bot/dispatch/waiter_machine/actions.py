import typing

from mubble.bot.cute_types import BaseCute
from mubble.bot.dispatch.handler.abc import ABCHandler

from .short_state import ShortState


class WaiterActions[Event: BaseCute](typing.TypedDict):
    on_miss: typing.NotRequired[ABCHandler[Event]]
    on_drop: typing.NotRequired[typing.Callable[[ShortState[Event]], None]]


__all__ = ("WaiterActions",)
