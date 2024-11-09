import typing

from mubble import node
from mubble.tools.i18n.abc import ABCTranslator

from .abc import ABCRule, with_caching_translations
from .node import NodeRule


class HasText(NodeRule):
    def __init__(self) -> None:
        super().__init__(node.text.Text)


class Text(ABCRule):
    def __init__(self, texts: str | list[str], *, ignore_case: bool = False) -> None:
        if not isinstance(texts, list):
            texts = [texts]
        self.texts = texts if not ignore_case else list(map(str.lower, texts))
        self.ignore_case = ignore_case

    def check(self, text: node.text.Text) -> bool:
        return (text if not self.ignore_case else text.lower()) in self.texts

    @with_caching_translations
    async def translate(self, translator: ABCTranslator) -> typing.Self:
        return self.__class__(
            texts=[translator.get(text) for text in self.texts],
            ignore_case=self.ignore_case,
        )


__all__ = ("HasText", "Text")
