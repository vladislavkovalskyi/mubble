from mubble.bot.rules.adapter.abc import ABCAdapter
from mubble.types.objects import Update
from mubble.bot.cute_types.update import UpdateCute
from mubble.bot.rules.adapter.errors import AdapterError
from mubble.result import Result, Ok
from mubble.api.abc import ABCAPI


class RawUpdateAdapter(ABCAdapter[Update, UpdateCute]):
    async def adapt(
        self, api: ABCAPI, update: Update
    ) -> Result[UpdateCute, AdapterError]:
        return Ok(update)
