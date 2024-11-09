import dataclasses

import typing_extensions as typing
from fntypes import Nothing, Option, Some
from vbml.patcher import Patcher

from mubble.api.api import API
from mubble.bot.cute_types.base import BaseCute
from mubble.bot.cute_types.update import UpdateCute
from mubble.bot.dispatch.abc import ABCDispatch
from mubble.bot.dispatch.handler.func import ErrorHandlerT, Func, FuncHandler
from mubble.bot.dispatch.view.box import (
    CallbackQueryView,
    ChatJoinRequestView,
    ChatMemberView,
    InlineQueryView,
    MessageView,
    PreCheckoutQueryView,
    RawEventView,
    ViewBox,
)
from mubble.modules import logger
from mubble.tools.error_handler.error_handler import ErrorHandler
from mubble.tools.global_context import MubbleContext
from mubble.types.enums import UpdateType
from mubble.types.objects import Update

if typing.TYPE_CHECKING:
    from mubble.bot.rules.abc import ABCRule

T = typing.TypeVar("T", default=typing.Any)
R = typing.TypeVar("R", covariant=True, default=typing.Any)
Event = typing.TypeVar("Event", bound=BaseCute)
P = typing.ParamSpec("P", default=...)

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
        PreCheckoutQueryView,
        RawEventView,
    ],
):
    _global_context: MubbleContext = dataclasses.field(
        init=False,
        default_factory=lambda: MubbleContext(),
    )

    def __repr__(self) -> str:
        return "Dispatch(%s)" % ", ".join(
            f"{k}={v!r}" for k, v in self.get_views().items()
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
        [Func[P, R]], FuncHandler[UpdateCute, Func[P, R], ErrorHandler[UpdateCute]]
    ]: ...

    @typing.overload
    def handle(
        self,
        *rules: "ABCRule",
        dataclass: type[T],
        is_blocking: bool = True,
    ) -> typing.Callable[
        [Func[P, R]], FuncHandler[UpdateCute, Func[P, R], ErrorHandler[T]]
    ]: ...

    @typing.overload
    def handle(
        self,
        *rules: "ABCRule",
        update_type: UpdateType,
        is_blocking: bool = True,
    ) -> typing.Callable[
        [Func[P, R]], FuncHandler[UpdateCute, Func[P, R], ErrorHandler[UpdateCute]]
    ]: ...

    @typing.overload
    def handle(
        self,
        *rules: "ABCRule",
        dataclass: type[T],
        update_type: UpdateType,
        is_blocking: bool = True,
    ) -> typing.Callable[
        [Func[P, R]], FuncHandler[UpdateCute, Func[P, R], ErrorHandler[T]]
    ]: ...

    @typing.overload
    def handle(
        self,
        *rules: "ABCRule",
        error_handler: ErrorHandlerT,
        is_blocking: bool = True,
    ) -> typing.Callable[
        [Func[P, R]], FuncHandler[UpdateCute, Func[P, R], ErrorHandlerT]
    ]: ...

    @typing.overload
    def handle(
        self,
        *rules: "ABCRule",
        update_type: UpdateType,
        error_handler: ErrorHandlerT,
        is_blocking: bool = True,
    ) -> typing.Callable[
        [Func[P, R]], FuncHandler[UpdateCute, Func[P, R], ErrorHandlerT]
    ]: ...

    @typing.overload
    def handle(
        self,
        *rules: "ABCRule",
        dataclass: type[typing.Any],
        error_handler: ErrorHandlerT,
        is_blocking: bool = True,
    ) -> typing.Callable[
        [Func[P, R]], FuncHandler[UpdateCute, Func[P, R], ErrorHandlerT]
    ]: ...

    @typing.overload
    def handle(
        self,
        *rules: "ABCRule",
        dataclass: type[typing.Any],
        update_type: UpdateType,
        error_handler: ErrorHandlerT,
        is_blocking: bool = True,
    ) -> typing.Callable[
        [Func[P, R]], FuncHandler[UpdateCute, Func[P, R], ErrorHandlerT]
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
        [Func[P, R]], FuncHandler[UpdateCute, Func[P, R], ErrorHandler[T]]
    ]: ...

    def handle(
        self,
        *rules: "ABCRule",
        update_type: UpdateType | None = None,
        dataclass: type[typing.Any] = DEFAULT_DATACLASS,
        error_handler: ErrorHandlerT | None = None,
        is_blocking: bool = True,
    ) -> typing.Callable[..., typing.Any]:
        def wrapper(func):
            handler = FuncHandler(
                func,
                list(rules),
                is_blocking=is_blocking,
                dataclass=dataclass,
                error_handler=error_handler or ErrorHandler(),
                update_type=update_type,
            )
            self.raw_event.handlers.append(handler)
            return handler

        return wrapper

    async def feed(self, event: Update, api: API) -> bool:
        logger.debug(
            "Processing update (update_id={}, update_type={!r})",
            event.update_id,
            event.update_type.name,
        )
        for view in self.get_views().values():
            if await view.check(event):
                logger.debug(
                    "Update (update_id={}, update_type={!r}) matched view {!r}.",
                    event.update_id,
                    event.update_type.name,
                    view,
                )
                if await view.process(event, api):
                    return True
        return False

    def load(self, external: typing.Self) -> None:
        view_external = external.get_views()
        for name, view in self.get_views().items():
            assert (
                name in view_external
            ), f"View {name!r} is undefined in external dispatch."
            view.load(view_external[name])
            setattr(external, name, view)

    def get_view(self, of_type: type[T]) -> Option[T]:
        for view in self.get_views().values():
            if isinstance(view, of_type):
                return Some(view)
        return Nothing()

    __call__ = handle


__all__ = ("Dispatch",)
