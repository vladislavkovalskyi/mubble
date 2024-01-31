import typing_extensions as typing

from mubble.api.abc import ABCAPI
from mubble.bot.cute_types import BaseCute
from mubble.bot.dispatch.context import Context
from mubble.bot.dispatch.process import check_rule
from mubble.modules import logger
from mubble.tools.error_handler import ABCErrorHandler, ErrorHandler
from mubble.types import Update

from .abc import ABCHandler

if typing.TYPE_CHECKING:
    from mubble.bot.rules import ABCRule

F = typing.TypeVar(
    "F", bound=typing.Callable[typing.Concatenate[typing.Any, ...], typing.Awaitable]
)
EventT = typing.TypeVar("EventT", bound=BaseCute)
ErrorHandlerT = typing.TypeVar(
    "ErrorHandlerT", bound=ABCErrorHandler, default=ErrorHandler
)


class FuncHandler(ABCHandler[EventT], typing.Generic[EventT, F, ErrorHandlerT]):
    def __init__(
        self,
        func: F,
        rules: list["ABCRule[EventT]"],
        is_blocking: bool = True,
        dataclass: type[typing.Any] | None = dict,
        error_handler: ErrorHandlerT | None = None,
    ):
        self.func = func
        self.is_blocking = is_blocking
        self.rules = rules
        self.dataclass = dataclass
        self.error_handler: ErrorHandlerT = error_handler or ErrorHandler()  # type: ignore
        self.ctx = Context()

    @property
    def on_error(self):
        return self.error_handler.catch

    async def check(
        self, api: ABCAPI, event: Update, ctx: Context | None = None
    ) -> bool:
        ctx = ctx or Context()
        preset_ctx = self.ctx.copy()
        self.ctx |= ctx
        for rule in self.rules:
            if not await check_rule(api, rule, event, self.ctx):
                logger.debug("Rule {!r} failed!", rule)
                self.ctx = preset_ctx
                return False
        return True

    async def run(self, event: EventT) -> typing.Any:
        if self.dataclass is not None:
            event = self.dataclass(**event.to_dict())
        return (
            await self.error_handler.run(self.func, event, event.api, self.ctx)
        ).unwrap()


__all__ = ("FuncHandler",)
