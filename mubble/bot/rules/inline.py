import abc

from mubble.bot.cute_types import InlineQueryCute
from mubble.bot.dispatch.context import Context
from mubble.bot.rules.abc import ABCRule
from mubble.bot.rules.adapter import EventAdapter

InlineQuery = InlineQueryCute


class InlineQueryRule(ABCRule[InlineQuery], abc.ABC):
    adapter = EventAdapter("inline_query", InlineQuery)

    @abc.abstractmethod
    async def check(self, query: InlineQuery, ctx: Context) -> bool:
        pass


class InlineQueryText(InlineQueryRule):
    def __init__(self, texts: str | list[str]) -> None:
        if isinstance(texts, str):
            texts = [texts]
        self.texts = texts

    async def check(self, query: InlineQuery, ctx: Context) -> bool:
        return query.query in self.texts


class LocationInlineQuery(InlineQueryRule):
    async def check(self, query: InlineQuery, ctx: Context) -> bool:
        return bool(query.location)


__all__ = ("InlineQueryRule", "InlineQueryText", "LocationInlineQuery")
