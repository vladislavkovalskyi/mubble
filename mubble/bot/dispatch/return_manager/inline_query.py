import typing

from mubble.bot.cute_types.inline_query import InlineQueryCute
from mubble.bot.dispatch.context import Context
from mubble.bot.dispatch.return_manager.abc import BaseReturnManager, register_manager


class InlineQueryReturnManager(BaseReturnManager[InlineQueryCute]):
    @register_manager(dict[str, typing.Any])
    @staticmethod
    async def dict_manager(value: dict[str, typing.Any], event: InlineQueryCute, ctx: Context) -> None:
        await event.answer(**value)


__all__ = ("InlineQueryReturnManager",)
