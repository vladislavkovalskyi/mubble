import asyncio
import datetime
import typing

from mubble.api.abc import ABCAPI
from mubble.bot.dispatch.context import Context
from mubble.bot.rules.abc import ABCRule
from mubble.tools.limited_dict import LimitedDict
from mubble.types import Update

from .middleware import WaiterMiddleware
from .short_state import Behaviour, EventModel, ShortState, ShortStateContext

if typing.TYPE_CHECKING:
    from mubble.bot.dispatch.view.abc import ABCStateView, BaseStateView

T = typing.TypeVar("T")

Identificator: typing.TypeAlias = str | int
Storage: typing.TypeAlias = dict[str, LimitedDict[Identificator, ShortState[EventModel]]]


class WaiterMachine:
    def __init__(self, *, max_storage_size: int = 1000) -> None:
        self.max_storage_size = max_storage_size
        self.storage: Storage = {}

    def __repr__(self) -> str:
        return "<{}: max_storage_size={}, storage={!r}>".format(
            self.__class__.__name__,
            self.max_storage_size,
            self.storage,
        )

    async def drop(
        self,
        state_view: "ABCStateView[EventModel]",
        id: Identificator,
        event: EventModel,
        update: Update,
        **context: typing.Any,
    ) -> None:
        view_name = state_view.__class__.__name__
        if view_name not in self.storage:
            raise LookupError("No record of view {!r} found.".format(view_name))

        short_state = self.storage[view_name].pop(id, None)
        if short_state is None:
            raise LookupError("Waiter with identificator {} is not found for view {!r}".format(id, view_name))

        short_state.cancel()
        await self.call_behaviour(
            state_view,
            event,
            update,
            behaviour=short_state.on_drop_behaviour,
            **context,
        )

    async def wait(
        self,
        state_view: "BaseStateView[EventModel]",
        linked: EventModel | tuple[ABCAPI, Identificator],
        *rules: ABCRule[EventModel],
        default: Behaviour[EventModel] | None = None,
        on_drop: Behaviour[EventModel] | None = None,
        exit: Behaviour[EventModel] | None = None,
        expiration: datetime.timedelta | float | None = None,
    ) -> ShortStateContext[EventModel]:
        if isinstance(expiration, int | float):
            expiration = datetime.timedelta(seconds=expiration)

        api: ABCAPI
        key: Identificator
        api, key = linked if isinstance(linked, tuple) else (linked.ctx_api, state_view.get_state_key(linked))  # type: ignore
        api, key = linked if isinstance(linked, tuple) else (linked.ctx_api, state_view.get_state_key(linked))  # type: ignore
        if not key:
            raise RuntimeError("Unable to get state key.")

        view_name = state_view.__class__.__name__
        event = asyncio.Event()
        short_state = ShortState[EventModel](
            key,
            api,
            event,
            rules,
            expiration=expiration,
            default_behaviour=default,
            on_drop_behaviour=on_drop,
            exit_behaviour=exit,
        )

        if view_name not in self.storage:
            state_view.middlewares.insert(0, WaiterMiddleware(self, state_view))
            self.storage[view_name] = LimitedDict(maxlimit=self.max_storage_size)

        if (deleted_short_state := self.storage[view_name].set(key, short_state)) is not None:
            deleted_short_state.cancel()

        await event.wait()
        self.storage[view_name].pop(key, None)
        assert short_state.context is not None
        return short_state.context

    async def call_behaviour(
        self,
        view: "ABCStateView[EventModel]",
        event: EventModel,
        update: Update,
        behaviour: Behaviour[EventModel] | None = None,
        **context: typing.Any,
    ) -> bool:
        # TODO: support view as a behaviour

        if behaviour is None:
            return False

        ctx = Context(**context)
        if await behaviour.check(event.api, update, ctx):
            await behaviour.run(event, ctx)
            return True

        return False


__all__ = ("WaiterMachine",)
