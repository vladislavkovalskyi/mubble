from .abc import ABCView
from mubble.bot.dispatch.handler import ABCHandler, FuncHandler
from mubble.bot.dispatch.waiter import Waiter
from mubble.bot.dispatch.middleware import ABCMiddleware
from mubble.bot.rules import ABCRule
from mubble.bot.cute_types import MessageCute
from mubble.api.abc import ABCAPI
from mubble.bot.dispatch.waiter import WithWaiter, DefaultWaiterHandler
from mubble.bot.dispatch.process import process_waiters, process_inner
from mubble.types import Update
import typing


class MessageView(ABCView, WithWaiter[int, MessageCute]):
    def __init__(self):
        self.auto_rules: list[ABCRule] = []
        self.handlers: list[ABCHandler[MessageCute]] = []
        self.middlewares: list[ABCMiddleware[MessageCute]] = []
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
        return bool(event.message)

    async def process(self, event: Update, api: ABCAPI):
        msg = MessageCute(**event.message.to_dict(), api=api)

        if await process_waiters(
            api, self.short_waiters, msg.chat.id, msg, event, msg.answer
        ):
            return

        return await process_inner(msg, event, self.middlewares, self.handlers)

    async def wait_for_message(
        self,
        chat_id: int,
        *rules: ABCRule,
        default: DefaultWaiterHandler | str | None = None,
    ) -> tuple["MessageCute", dict]:
        return await self.wait_for_answer(
            chat_id, *self.auto_rules, *rules, default=default
        )
