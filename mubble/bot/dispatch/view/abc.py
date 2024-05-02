import typing
from abc import ABC, abstractmethod

from fntypes.co import Nothing, Some

from mubble.api.abc import ABCAPI
from mubble.bot.cute_types.base import BaseCute
from mubble.bot.dispatch.handler.abc import ABCHandler
from mubble.bot.dispatch.handler.func import FuncHandler
from mubble.bot.dispatch.middleware.abc import ABCMiddleware
from mubble.bot.dispatch.process import process_inner
from mubble.bot.dispatch.return_manager.abc import ABCReturnManager
from mubble.bot.rules.abc import ABCRule
from mubble.model import Model
from mubble.msgspec_utils import Option
from mubble.tools.error_handler.error_handler import ABCErrorHandler, ErrorHandler
from mubble.types.objects import Update

EventType = typing.TypeVar("EventType", bound=BaseCute)
ErrorHandlerT = typing.TypeVar("ErrorHandlerT", bound=ABCErrorHandler)
MiddlewareT = typing.TypeVar("MiddlewareT", bound=ABCMiddleware)

FuncType: typing.TypeAlias = typing.Callable[
    typing.Concatenate[EventType, ...],
    typing.Coroutine[typing.Any, typing.Any, typing.Any],
]


class ABCView(ABC):
    @abstractmethod
    async def check(self, event: Update) -> bool:
        pass

    @abstractmethod
    async def process(self, event: Update, api: ABCAPI):
        pass

    @abstractmethod
    def load(self, external: typing.Self) -> None:
        pass


class ABCStateView(ABCView, typing.Generic[EventType]):
    @abstractmethod
    def get_state_key(self, event: EventType) -> int | None:
        pass

    def __repr__(self) -> str:
        return "<{!r}: {}>".format(
            self.__class__.__name__,
            ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items()),
        )


class BaseView(ABCView, typing.Generic[EventType]):
    auto_rules: list[ABCRule[EventType]]
    handlers: list[ABCHandler[EventType]]
    middlewares: list[ABCMiddleware[EventType]]
    return_manager: ABCReturnManager[EventType]

    @classmethod
    def get_event_type(cls) -> Option[type[EventType]]:
        for base in cls.__dict__.get("__orig_bases__", ()):
            if issubclass(typing.get_origin(base) or base, ABCView):
                for generic_type in typing.get_args(base):
                    if issubclass(
                        typing.get_origin(generic_type) or generic_type, BaseCute
                    ):
                        return Some(generic_type)
        return Nothing()

    @classmethod
    def get_raw_event(cls, update: Update) -> Option[Model]:
        match update.update_type:
            case Some(update_type):
                return getattr(update, update_type.value)
            case _:
                return Nothing()
    
    @typing.overload
    def __call__(
        self,
        *rules: ABCRule[EventType],
    ) -> typing.Callable[[FuncType[EventType]], FuncHandler[EventType, FuncType[EventType], ErrorHandler]]:
        ...
    
    @typing.overload
    def __call__(
        self,
        *rules: ABCRule[EventType],
        error_handler: ErrorHandlerT,
        is_blocking: bool = True,
    ) -> typing.Callable[[FuncType[EventType]], FuncHandler[EventType, FuncType[EventType], ErrorHandlerT]]:
        ...

    @typing.overload
    def __call__(
        self,
        *rules: ABCRule[EventType],
        error_handler: typing.Literal[None] = None,
        is_blocking: bool = True,
    ) -> typing.Callable[[FuncType[EventType]], FuncHandler[EventType, FuncType[EventType], ErrorHandler]]:
        ...

    def __call__(  # type: ignore
        self,
        *rules: ABCRule[EventType],
        error_handler: ABCErrorHandler | None = None,
        is_blocking: bool = True,
    ):
        def wrapper(func: FuncType[EventType]):
            func_handler = FuncHandler(
                func,
                [*self.auto_rules, *rules],
                is_blocking=is_blocking,
                dataclass=None,
            )
            self.handlers.append(func_handler)
            return func_handler

        return wrapper

    def register_middleware(self, *args: typing.Any, **kwargs: typing.Any):
        def wrapper(cls: type[MiddlewareT]) -> type[MiddlewareT]:
            self.middlewares.append(cls(*args, **kwargs))
            return cls

        return wrapper

    async def check(self, event: Update) -> bool:
        match self.get_raw_event(event):
            case Some(e) if issubclass(
                self.get_event_type().expect(
                    "{!r} has no event type in generic.".format(self.__class__.__name__),
                ),
                e.__class__,
            ):
                return True
            case _:
                return False

    async def process(self, event: Update, api: ABCAPI) -> bool:
        return await process_inner(
            self.get_event_type()
            .unwrap()
            .from_update(
                update=self.get_raw_event(event).unwrap(),
                bound_api=api,
            ),
            event,
            self.middlewares,
            self.handlers,
            self.return_manager,
        )

    def load(self, external: typing.Self) -> None:
        self.auto_rules.extend(external.auto_rules)
        self.handlers.extend(external.handlers)
        self.middlewares.extend(external.middlewares)


class BaseStateView(ABCStateView[EventType], BaseView[EventType], ABC, typing.Generic[EventType]):
    @abstractmethod
    def get_state_key(self, event: EventType) -> int | None:
        pass


__all__ = (
    "ABCView",
    "ABCStateView",
    "BaseView",
    "BaseStateView",
)
