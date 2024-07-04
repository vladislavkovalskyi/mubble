from mubble.bot.cute_types.update import UpdateCute
from mubble.bot.dispatch.context import Context
from mubble.types.enums import UpdateType

from .abc import ABCRule, EventCute


class IsUpdate(ABCRule[EventCute]):
    def __init__(self, update_type: UpdateType, /) -> None:
        self.update_type = update_type

    async def check(self, event: UpdateCute, ctx: Context) -> bool:
        return event.update_type == self.update_type


__all__ = ("IsUpdate",)
