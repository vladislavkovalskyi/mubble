import typing

from mubble.api.api import API
from mubble.bot.cute_types.base import BaseCute
from mubble.bot.cute_types.update import UpdateCute
from mubble.bot.dispatch.context import Context
from mubble.bot.dispatch.handler.func import Func, FuncHandler
from mubble.bot.dispatch.process import process_inner
from mubble.bot.dispatch.view.abc import ABCEventRawView
from mubble.bot.dispatch.view.base import BaseView
from mubble.bot.rules.abc import ABCRule
from mubble.tools.error_handler.error_handler import ABCErrorHandler, ErrorHandler
from mubble.types.enums import UpdateType
from mubble.types.objects import Update


class RawEventView(ABCEventRawView[UpdateCute], BaseView[UpdateCute]):
    @typing.overload
    def __call__[**P, R](
        self,
        *rules: ABCRule,
        update_type: UpdateType,
        final: bool = True,
    ) -> typing.Callable[
        [Func[P, R]],
        FuncHandler[BaseCute[typing.Any], Func[P, R], ErrorHandler[BaseCute[typing.Any]]],
    ]: ...

    @typing.overload
    def __call__[**P, Dataclass, R](
        self,
        *rules: ABCRule,
        dataclass: type[Dataclass],
        final: bool = True,
    ) -> typing.Callable[[Func[P, R]], FuncHandler[Dataclass, Func[P, R], ErrorHandler[Dataclass]]]: ...

    @typing.overload
    def __call__[**P, Dataclass, R](
        self,
        *rules: ABCRule,
        update_type: UpdateType,
        dataclass: type[Dataclass],
        final: bool = True,
    ) -> typing.Callable[[Func[P, R]], FuncHandler[Dataclass, Func[P, R], ErrorHandler[Dataclass]]]: ...

    @typing.overload
    def __call__[**P, ErrorHandlerT: ABCErrorHandler, R](
        self,
        *rules: ABCRule,
        error_handler: ErrorHandlerT,
        final: bool = True,
    ) -> typing.Callable[
        [Func[P, R]],
        FuncHandler[BaseCute[typing.Any], Func[P, R], ErrorHandlerT],
    ]: ...

    @typing.overload
    def __call__[**P, ErrorHandlerT: ABCErrorHandler, R](
        self,
        *rules: ABCRule,
        error_handler: ErrorHandlerT,
        update_type: UpdateType,
        final: bool = True,
    ) -> typing.Callable[
        [Func[P, R]],
        FuncHandler[BaseCute[typing.Any], Func[P, R], ErrorHandlerT],
    ]: ...

    @typing.overload
    def __call__[**P, Dataclass, ErrorHandlerT: ABCErrorHandler, R](
        self,
        *rules: ABCRule,
        update_type: UpdateType,
        dataclass: type[Dataclass],
        error_handler: ErrorHandlerT,
        final: bool = True,
    ) -> typing.Callable[[Func[P, R]], FuncHandler[Dataclass, Func[P, R], ErrorHandlerT]]: ...

    def __call__(
        self,
        *rules: ABCRule,
        update_type: UpdateType | None = None,
        dataclass: type[typing.Any] | None = None,
        error_handler: ABCErrorHandler | None = None,
        final: bool = True,
    ) -> typing.Callable[..., typing.Any]:
        def wrapper(func: typing.Callable[..., typing.Any]):
            func_handler = FuncHandler(
                func,
                rules=[*self.auto_rules, *rules],
                final=final,
                dataclass=dataclass,
                error_handler=error_handler or ErrorHandler(),
                update_type=update_type,
            )
            self.handlers.append(func_handler)
            return func_handler

        return wrapper

    async def check(self, event: Update) -> bool:
        return bool(self.handlers) or bool(self.middlewares)

    async def process(self, event: Update, api: API, context: Context) -> bool:
        return await process_inner(
            api,
            UpdateCute.from_update(event, bound_api=api),
            event,
            context,
            self.middlewares,
            self.handlers,
            self.return_manager,
        )


__all__ = ("RawEventView",)
