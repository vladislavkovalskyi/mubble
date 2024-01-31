from mubble.api.abc import ABCAPI
from mubble.bot.cute_types.update import UpdateCute
from mubble.bot.rules.adapter.abc import ABCAdapter
from mubble.bot.rules.adapter.errors import AdapterError
from mubble.result import Ok, Result
from mubble.types.objects import Update


class RawUpdateAdapter(ABCAdapter[Update, UpdateCute]):
    async def adapt(
        self,
        api: ABCAPI,
        update: Update,
    ) -> Result[UpdateCute, AdapterError]:
        if not isinstance(update, UpdateCute):
            return Ok(UpdateCute.from_update(update, api))
        return Ok(update)


__all__ = ("RawUpdateAdapter",)
