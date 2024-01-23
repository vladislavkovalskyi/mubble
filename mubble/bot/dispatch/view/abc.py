from abc import ABC, abstractmethod
from mubble.api.abc import ABCAPI
from mubble.bot.dispatch.middleware.abc import ABCMiddleware
from mubble.bot.dispatch.handler.abc import ABCHandler
from mubble.bot.dispatch.waiter import Waiter
from mubble.bot.rules.abc import ABCRule
from mubble.types import Update
import typing

T = typing.TypeVar("T", bound=ABCMiddleware)


class ABCView(ABC):
    auto_rules: list[ABCRule]
    handlers: list[ABCHandler]
    middlewares: list[ABCMiddleware]
    short_waiters: dict[int, Waiter]

    @abstractmethod
    async def check(self, event: Update) -> bool:
        pass

    @abstractmethod
    async def process(self, event: Update, api: ABCAPI):
        pass

    def load(self, external: typing.Self):
        self.auto_rules.append(external.auto_rules)
        self.handlers.extend(external.handlers)
        self.middlewares.extend(external.middlewares)
        self.short_waiters.update(external.short_waiters)

    def register_middleware(self, *args, **kwargs):
        def wrapper(middleware: typing.Type[T]) -> typing.Type[T]:
            self.middlewares.append(middleware(*args, **kwargs))
            return middleware

        return wrapper
