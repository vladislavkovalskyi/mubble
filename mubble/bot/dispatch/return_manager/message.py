import typing

from mubble.bot.cute_types import MessageCute
from mubble.bot.dispatch.context import Context
from mubble.tools.formatting import HTMLFormatter

from .abc import BaseReturnManager, register_manager


class MessageReturnManager(BaseReturnManager[MessageCute]):  
    @register_manager(str)
    @staticmethod
    async def str_manager(value: str, event: MessageCute, ctx: Context) -> None:
        await event.answer(value)
    
    @register_manager(list | tuple)
    @staticmethod
    async def seq_manager(value: list[str] | tuple[str, ...], event: MessageCute, ctx: Context) -> None:
        for message in value:
            await event.answer(message)
    
    @register_manager(dict)
    @staticmethod
    async def dict_manager(value: dict[str, typing.Any], event: MessageCute, ctx: Context) -> None:
        await event.answer(**value)

    @register_manager(HTMLFormatter)
    @staticmethod
    async def htmlformatter_manager(value: HTMLFormatter, event: MessageCute, ctx: Context) -> None:
        await event.answer(value, parse_mode=HTMLFormatter.PARSE_MODE)


__all__ = ("MessageReturnManager",)
