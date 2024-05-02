from mubble.bot.dispatch.context import Context
from mubble.tools.i18n.base import ABCTranslator

from .abc import ABC, Message, MessageRule, with_caching_translations


class HasText(MessageRule):
    async def check(self, message: Message, ctx: Context) -> bool:
        return bool(message.text)


class TextMessageRule(MessageRule, ABC, requires=[HasText()]):
    pass


class Text(TextMessageRule):
    def __init__(self, texts: str | list[str], *, ignore_case: bool = False) -> None:
        if not isinstance(texts, list):
            texts = [texts]
        self.texts = list(map(str.lower, texts)) if ignore_case else texts
        self.ignore_case = ignore_case

    async def check(self, message: Message, ctx: Context) -> bool:
        text = message.text.unwrap()
        return (text.lower() if self.ignore_case else text) in self.texts

    @with_caching_translations
    async def translate(self, translator: ABCTranslator) -> "Text":
        return Text(
            texts=[translator.get(text) for text in self.texts],
            ignore_case=self.ignore_case,
        )


__all__ = ("HasText", "Text", "TextMessageRule")
