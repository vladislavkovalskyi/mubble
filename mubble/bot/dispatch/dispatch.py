import asyncio
import dataclasses
import typing

from vbml.patcher import Patcher

from mubble.api.abc import ABCAPI
from mubble.bot.cute_types.base import BaseCute
from mubble.bot.cute_types.update import UpdateCute
from mubble.bot.dispatch.context import Context
from mubble.bot.dispatch.handler.abc import ABCHandler
from mubble.bot.dispatch.handler.func import ErrorHandlerT, FuncHandler
from mubble.modules import logger
from mubble.tools.error_handler.error_handler import ErrorHandler
from mubble.tools.global_context import MubbleContext
from mubble.types.enums import UpdateType
from mubble.types.objects import Update

from .abc import ABCDispatch
from .view.box import (
    CallbackQueryView,
    ChatJoinRequestView,
    ChatMemberView,
    InlineQueryView,
    MessageView,
    RawEventView,
    ViewBox,
)

if typing.TYPE_CHECKING:
    from mubble.bot.rules.abc import ABCRule

T = typing.TypeVar("T")
Handler = typing.Callable[
    typing.Concatenate[T, ...], typing.Coroutine[typing.Any, typing.Any, typing.Any]
]
Event = typing.TypeVar("Event", bound=BaseCute)

DEFAULT_DATACLASS: typing.Final[type[Update]] = Update


@dataclasses.dataclass(repr=False, kw_only=True)
class Dispatch(
    ABCDispatch,
    ViewBox[
        CallbackQueryView,
        ChatJoinRequestView,
        ChatMemberView,
        InlineQueryView,
        MessageView,
        RawEventView,
    ],
):
    default_handlers: list[ABCHandler] = dataclasses.field(
        init=False,
        default_factory=lambda: [],
    )
    _global_context: MubbleContext = dataclasses.field(
        init=False,
        default_factory=lambda: MubbleContext(),
    )

    def __repr__(self) -> str:
        return "Dispatch(%s)" % ", ".join(
            f"{k}={v!r}" for k, v in self.__dict__.items()
        )

    @property
    def global_context(self) -> MubbleContext:
        return self._global_context

    @property
    def patcher(self) -> Patcher:
        """Alias `patcher` to get `vbml.Patcher` from the global context."""

        return self.global_context.vbml_patcher

    @typing.overload
    def handle(
        self,
        *rules: "ABCRule",
        is_blocking: bool = True,
    ) -> typing.Callable[
        [Handler[T]], FuncHandler[UpdateCute, Handler[T], ErrorHandler]
    ]: ...

    @typing.overload
    def handle(
        self,
        *rules: "ABCRule",
        dataclass: type[T],
        is_blocking: bool = True,
    ) -> typing.Callable[
        [Handler[T]], FuncHandler[UpdateCute, Handler[T], ErrorHandler]
    ]: ...

    @typing.overload
    def handle(
        self,
        *rules: "ABCRule",
        update_type: UpdateType,
        is_blocking: bool = True,
    ) -> typing.Callable[
        [Handler[T]], FuncHandler[UpdateCute, Handler[T], ErrorHandler]
    ]: ...

    @typing.overload
    def handle(
        self,
        *rules: "ABCRule",
        dataclass: type[T],
        update_type: UpdateType,
        is_blocking: bool = True,
    ) -> typing.Callable[
        [Handler[T]], FuncHandler[UpdateCute, Handler[T], ErrorHandler]
    ]: ...

    @typing.overload
    def handle(
        self,
        *rules: "ABCRule",
        error_handler: ErrorHandlerT,
        is_blocking: bool = True,
    ) -> typing.Callable[
        [Handler[T]], FuncHandler[UpdateCute, Handler[T], ErrorHandlerT]
    ]: ...

    @typing.overload
    def handle(
        self,
        *rules: "ABCRule",
        update_type: UpdateType,
        error_handler: ErrorHandlerT,
        is_blocking: bool = True,
    ) -> typing.Callable[
        [Handler[T]], FuncHandler[UpdateCute, Handler[T], ErrorHandlerT]
    ]: ...

    @typing.overload
    def handle(
        self,
        *rules: "ABCRule",
        dataclass: type[T],
        error_handler: ErrorHandlerT,
        is_blocking: bool = True,
    ) -> typing.Callable[
        [Handler[T]], FuncHandler[UpdateCute, Handler[T], ErrorHandlerT]
    ]: ...

    @typing.overload
    def handle(
        self,
        *rules: "ABCRule",
        dataclass: type[T],
        update_type: UpdateType,
        error_handler: ErrorHandlerT,
        is_blocking: bool = True,
    ) -> typing.Callable[
        [Handler[T]], FuncHandler[UpdateCute, Handler[T], ErrorHandlerT]
    ]: ...

    @typing.overload
    def handle(
        self,
        *rules: "ABCRule",
        update_type: UpdateType | None = None,
        dataclass: type[T] = DEFAULT_DATACLASS,
        error_handler: typing.Literal[None] = None,
        is_blocking: bool = True,
    ) -> typing.Callable[
        [Handler[T]], FuncHandler[UpdateCute, Handler[T], ErrorHandler]
    ]: ...

    def handle(
        self,
        *rules: "ABCRule",
        update_type: UpdateType | None = None,
        dataclass: type[typing.Any] = DEFAULT_DATACLASS,
        error_handler: ErrorHandlerT | None = None,
        is_blocking: bool = True,
    ):
        def wrapper(func: typing.Callable):
            handler = FuncHandler(
                func,
                list(rules),
                is_blocking=is_blocking,
                dataclass=dataclass,
                error_handler=error_handler or ErrorHandler(),
                update_type=update_type,
            )
            self.default_handlers.append(handler)
            return handler

        return wrapper

    async def feed(self, event: Update, api: ABCAPI) -> bool:
        logger.debug("Processing update (update_id={})", event.update_id)
        await self.raw_event.process(event, api)

        for view in self.get_views().values():
            if await view.check(event):
                logger.debug(
                    "Update (update_id={}) matched view {!r}.",
                    event.update_id,
                    view,
                )
                if await view.process(event, api):
                    return True

        ctx = Context(raw_update=event)
        loop = asyncio.get_running_loop()
        found = False
        for handler in self.default_handlers:
            if await handler.check(api, event, ctx):
                found = True
                loop.create_task(handler.run(api, event, ctx))
                if handler.is_blocking:
                    break
        return found

    def load(self, external: typing.Self) -> None:
        view_external = external.get_views()
        for name, view in self.get_views().items():
            assert (
                name in view_external
            ), f"View {name!r} is undefined in external dispatch."
            view.load(view_external[name])
            setattr(external, name, view)

    __call__ = handle


__all__ = ("Dispatch",)
