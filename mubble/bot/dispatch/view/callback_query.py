from mubble.bot.dispatch.middleware.abc import ABCMiddleware
from .abc import ABCView
from mubble.bot.dispatch.handler import ABCHandler, FuncHandler
from mubble.bot.dispatch.waiter import Waiter
from mubble.bot.rules import ABCRule
from mubble.bot.cute_types import CallbackQueryCute
from mubble.api.abc import ABCAPI
from mubble.bot.dispatch.waiter import WithWaiter
from mubble.bot.dispatch.process import process_waiters, process_inner
from mubble.types import Update
import typing


class CallbackQueryView(ABCView, WithWaiter[int, CallbackQueryCute]):
    def __init__(self):
        self.auto_rules: list[ABCRule] = []
        self.handlers: list[ABCHandler[CallbackQueryCute]] = []
        self.middlewares: list[ABCMiddleware[CallbackQueryCute]] = []
        self.short_waiters: dict[int, Waiter] = {}

    def __call__(self, *rules: ABCRule, is_blocking: bool = True):
        def wrapper(func: typing.Callable[..., typing.Coroutine]):
            self.handlers.append(
                FuncHandler(
                    func, [*self.auto_rules, *rules], is_blocking, dataclass=None
                )
            )
            return func

        return wrapper

    async def check(self, event: Update) -> bool:
        return bool(event.callback_query)

    async def process(self, event: Update, api: ABCAPI):
        query = CallbackQueryCute(**event.callback_query.to_dict(), api=api)

        if await process_waiters(
            api,
            self.short_waiters,
            query.message.message_id,
            query,
            event,
            query.answer,
        ):
            return

        return await process_inner(query, event, self.middlewares, self.handlers)
