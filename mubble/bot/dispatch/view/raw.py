import typing

from mubble.api.api import API
from mubble.bot.cute_types.update import UpdateCute
from mubble.bot.dispatch.handler.func import Func, FuncHandler
from mubble.bot.dispatch.process import process_inner
from mubble.bot.dispatch.view.abc import ABCEventRawView
from mubble.bot.dispatch.view.base import BaseView
from mubble.bot.rules.abc import ABCRule
from mubble.tools.error_handler.error_handler import ABCErrorHandler, ErrorHandler
from mubble.types.enums import UpdateType
from mubble.types.objects import Update


class RawEventView(ABCEventRawView[UpdateCute], BaseView[UpdateCute]):
    def __init__(self) -> None:
        self.auto_rules = []
        self.handlers = []
        self.middlewares = []
        self.return_manager = None

    @typing.overload
    def __call__[**P, R](
        self,
        update_type: UpdateType,
        *rules: ABCRule,
    ) -> typing.Callable[
        [Func[P, R]],
        FuncHandler[UpdateCute, Func[P, R], ErrorHandler[UpdateCute]],
    ]: ...

    @typing.overload
    def __call__[**P, Dataclass, R](
        self,
        update_type: UpdateType,
        *rules: ABCRule,
        dataclass: type[Dataclass],
    ) -> typing.Callable[[Func[P, R]], FuncHandler[UpdateCute, Func[P, R], ErrorHandler[Dataclass]]]: ...

    @typing.overload
    def __call__[**P, ErrorHandlerT: ABCErrorHandler, R](
        self,
        update_type: UpdateType,
        *rules: ABCRule,
        error_handler: ErrorHandlerT,
    ) -> typing.Callable[
        [Func[P, R]],
        FuncHandler[UpdateCute, Func[P, R], ErrorHandlerT],
    ]: ...

    @typing.overload
    def __call__[**P, ErrorHandlerT: ABCErrorHandler, R](
        self,
        update_type: UpdateType,
        *rules: ABCRule,
        dataclass: type[typing.Any],
        error_handler: ErrorHandlerT,
        is_blocking: bool = True,
    ) -> typing.Callable[[Func[P, R]], FuncHandler[UpdateCute, Func[P, R], ErrorHandlerT]]: ...

    @typing.overload
    def __call__[**P, R](
        self,
        update_type: UpdateType,
        *rules: ABCRule,
        dataclass: None = None,
        error_handler: None = None,
        is_blocking: bool = True,
    ) -> typing.Callable[
        [Func[P, R]],
        FuncHandler[UpdateCute, Func[P, R], ErrorHandler[UpdateCute]],
    ]: ...

    def __call__(
        self,
        update_type: UpdateType,
        *rules: ABCRule,
        dataclass: type[typing.Any] | None = None,
        error_handler: ABCErrorHandler | None = None,
        is_blocking: bool = True,
    ) -> typing.Callable[..., typing.Any]:
        def wrapper(func):
            func_handler = FuncHandler(
                func,
                rules=[*self.auto_rules, *rules],
                is_blocking=is_blocking,
                dataclass=dataclass,
                error_handler=error_handler or ErrorHandler(),
                update_type=update_type,
            )
            self.handlers.append(func_handler)
            return func_handler

        return wrapper

    async def check(self, event: Update) -> bool:
        return bool(self.handlers) or bool(self.middlewares)

    async def process(self, event: Update, api: API) -> bool:
        return await process_inner(
            api,
            UpdateCute.from_update(event, bound_api=api),
            event,
            self.middlewares,
            self.handlers,
            self.return_manager,
        )


__all__ = ("RawEventView",)
