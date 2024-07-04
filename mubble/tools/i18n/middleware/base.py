import typing
from abc import abstractmethod

from mubble.bot.cute_types.base import BaseCute
from mubble.bot.dispatch.middleware import ABCMiddleware
from mubble.tools.i18n import ABCI18n, I18nEnum

T = typing.TypeVar("T", bound=BaseCute)


class ABCTranslatorMiddleware(ABCMiddleware[T]):
    def __init__(self, i18n: ABCI18n):
        self.i18n = i18n

    @abstractmethod
    async def get_locale(self, event: T) -> str:
        pass

    async def pre(self, event: T, ctx: dict) -> bool:
        ctx[I18nEnum.I18N] = self.i18n.get_translator_by_locale(await self.get_locale(event))
        return True


__all__ = ("ABCTranslatorMiddleware",)
