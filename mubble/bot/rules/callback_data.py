from .abc import ABCRule
from mubble.modules import json
from mubble.bot.cute_types import CallbackQueryCute
from mubble.bot.rules.adapter import EventAdapter
from .markup import Markup, check_string
import msgspec
import vbml
import abc
import typing

CallbackQuery = CallbackQueryCute
PatternLike = str | vbml.Pattern


class CallbackQueryRule(ABCRule[CallbackQuery], abc.ABC):
    adapter = EventAdapter("callback_query", CallbackQuery)

    @abc.abstractmethod
    async def check(self, event: CallbackQuery, ctx: dict) -> bool:
        pass


class CallbackData(CallbackQueryRule):
    def __init__(self, values: str | list[str]):
        self.values = values

    async def check(self, event: CallbackQuery, ctx: dict) -> bool:
        return event.data in self.values


class CallbackDataJson(CallbackQueryRule):
    def __init__(self, d: dict):
        self.d = d

    async def check(self, event: CallbackQuery, ctx: dict) -> bool:
        if not event.data:
            return False
        try:
            return json.loads(event.data) == self.d
        except:
            return False


class CallbackDataJsonModel(CallbackQueryRule):
    def __init__(self, model: typing.Type[msgspec.Struct]):
        self.decoder = msgspec.json.Decoder(type=model)

    async def check(self, event: CallbackQuery, ctx: dict) -> bool:
        try:
            ctx["data"] = self.decoder.decode(event.data.encode())
            return True
        except msgspec.DecodeError:
            return False


class CallbackDataMarkup(CallbackQueryRule):
    def __init__(self, patterns: PatternLike | list[PatternLike]):
        self.patterns = Markup(patterns).patterns

    async def check(self, event: CallbackQuery, ctx: dict) -> bool:
        return check_string(self.patterns, event.data, ctx)
