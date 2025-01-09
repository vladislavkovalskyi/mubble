import asyncio
import datetime
import typing

from mubble.bot.cute_types.base import BaseCute
from mubble.bot.dispatch.abc import ABCDispatch
from mubble.bot.dispatch.context import Context
from mubble.bot.dispatch.view.base import BaseStateView, BaseView
from mubble.bot.dispatch.waiter_machine.middleware import (
    INITIATOR_CONTEXT_KEY,
    WaiterMiddleware,
)
from mubble.bot.dispatch.waiter_machine.short_state import (
    ShortState,
    ShortStateContext,
)
from mubble.bot.rules.abc import ABCRule
from mubble.tools.lifespan import Lifespan
from mubble.tools.limited_dict import LimitedDict

from .actions import WaiterActions
from .hasher import Hasher, StateViewHasher

type Storage[Event: BaseCute, HasherData] = dict[
    Hasher[Event, HasherData],
    LimitedDict[typing.Hashable, ShortState[Event]],
]
type HasherWithData[Event: BaseCute, Data] = tuple[Hasher[Event, Data], Data]

WEEK: typing.Final[datetime.timedelta] = datetime.timedelta(days=7)


class ContextUnpackProto[Ts: tuple[typing.Any, ...]](typing.Protocol):
    def __call__(self, context: Context) -> Ts: ...


def unpack_to_context(context: Context) -> tuple[Context]:
    return (context,)


def no_unpack(_: Context) -> tuple[()]:
    return ()


class WaiterMachine:
    def __init__(
        self,
        dispatch: ABCDispatch | None = None,
        *,
        max_storage_size: int = 1000,
        base_state_lifetime: datetime.timedelta = WEEK,
    ) -> None:
        self.dispatch = dispatch
        self.max_storage_size = max_storage_size
        self.base_state_lifetime = base_state_lifetime
        self.storage: Storage = {}

    def __repr__(self) -> str:
        return "<{}: max_storage_size={}, base_state_lifetime={!r}>".format(
            self.__class__.__name__,
            self.max_storage_size,
            self.base_state_lifetime,
        )

    def create_middleware[
        Event: BaseCute
    ](self, view: BaseStateView[Event]) -> WaiterMiddleware[Event]:
        hasher = StateViewHasher(view)
        self.storage[hasher] = LimitedDict(maxlimit=self.max_storage_size)
        return WaiterMiddleware(self, hasher)

    async def drop_all(self) -> None:
        """Drops all waiters in storage."""

        for hasher in self.storage.copy():
            for ident, short_state in self.storage[hasher].items():
                if short_state.context:
                    await self.drop(hasher, ident)
                else:
                    await short_state.cancel()

            del self.storage[hasher]

    async def drop[
        Event: BaseCute, HasherData
    ](
        self,
        hasher: Hasher[Event, HasherData],
        data: HasherData,
        **context: typing.Any,
    ) -> None:
        if hasher not in self.storage:
            raise LookupError("No record of hasher {!r} found.".format(hasher))

        waiter_id: typing.Hashable = hasher.get_hash_from_data(data).expect(
            RuntimeError("Couldn't create hash from data"),
        )
        short_state = self.storage[hasher].pop(waiter_id, None)
        if short_state is None:
            raise LookupError(
                "Waiter with identificator {} is not found for hasher {!r}.".format(
                    waiter_id, hasher
                )
            )

        if on_drop := short_state.actions.get("on_drop"):
            on_drop(short_state, **context)

        await short_state.cancel()

    async def wait_from_event[
        Event: BaseCute
    ](
        self,
        view: BaseStateView[Event],
        event: Event,
        *,
        filter: ABCRule | None = None,
        release: ABCRule | None = None,
        lifetime: datetime.timedelta | float | None = None,
        lifespan: Lifespan = Lifespan(),
        **actions: typing.Unpack[WaiterActions[Event]],
    ) -> ShortStateContext[Event]:
        hasher = StateViewHasher(view)
        return await self.wait(
            hasher=hasher,
            data=hasher.get_data_from_event(event).expect(
                RuntimeError("Hasher couldn't create data from event."),
            ),
            filter=filter,
            release=release,
            lifetime=lifetime,
            lifespan=lifespan,
            **actions,
        )

    async def wait[
        Event: BaseCute, HasherData
    ](
        self,
        hasher: Hasher[Event, HasherData],
        data: HasherData,
        *,
        filter: ABCRule | None = None,
        release: ABCRule | None = None,
        lifetime: datetime.timedelta | float | None = None,
        lifespan: Lifespan = Lifespan(),
        **actions: typing.Unpack[WaiterActions[Event]],
    ) -> ShortStateContext[Event]:
        if isinstance(lifetime, int | float):
            lifetime = datetime.timedelta(seconds=lifetime)

        event = asyncio.Event()
        short_state = ShortState[Event](
            event,
            actions,
            release=release,
            filter=filter,
            lifetime=lifetime or self.base_state_lifetime,
        )
        waiter_hash = hasher.get_hash_from_data(data).expect(
            RuntimeError("Hasher couldn't create hash.")
        )

        if hasher not in self.storage:
            if self.dispatch:
                view: BaseView[Event] = self.dispatch.get_view(
                    hasher.view_class
                ).expect(
                    RuntimeError(
                        f"View {hasher.view_class.__name__!r} is not defined in dispatch."
                    ),
                )
                view.middlewares.insert(0, WaiterMiddleware(self, hasher))
            self.storage[hasher] = LimitedDict(maxlimit=self.max_storage_size)

        if (
            deleted_short_state := self.storage[hasher].set(waiter_hash, short_state)
        ) is not None:
            await deleted_short_state.cancel()

        async with lifespan:
            await event.wait()

        self.storage[hasher].pop(waiter_hash, None)

        if short_state.context is None:
            raise LookupError("No context in short_state.")
        return short_state.context

    async def wait_many[
        RestEvent: BaseCute[typing.Any], Data, Ts: tuple[typing.Any, ...]
    ](
        self,
        *hashers: HasherWithData[RestEvent, Data],
        filter: ABCRule | None = None,
        release: ABCRule | None = None,
        lifetime: datetime.timedelta | float | None = None,
        lifespan: Lifespan = Lifespan(),
        unpack: ContextUnpackProto[Ts] = unpack_to_context,
        **actions: typing.Unpack[WaiterActions[BaseCute[typing.Any]]],
    ) -> tuple[HasherWithData[RestEvent, Data], RestEvent, typing.Unpack[Ts]]:
        if isinstance(lifetime, int | float):
            lifetime = datetime.timedelta(seconds=lifetime)

        event = asyncio.Event()
        short_state = ShortState(
            event,
            actions,
            release=release,
            filter=filter,
            lifetime=lifetime or self.base_state_lifetime,
        )
        waiter_hashes: dict[Hasher[RestEvent, Data], typing.Hashable] = {}

        for hasher, data in hashers:
            waiter_hash = hasher.get_hash_from_data(data).expect(
                RuntimeError("Hasher couldn't create hash.")
            )

            if hasher not in self.storage:
                if self.dispatch:
                    view = self.dispatch.get_view(hasher.view_class).expect(
                        RuntimeError(
                            f"View {hasher.view_class.__name__!r} is not defined in dispatch."
                        ),
                    )
                    view.middlewares.insert(0, WaiterMiddleware(self, hasher))
                self.storage[hasher] = LimitedDict(maxlimit=self.max_storage_size)

            if (
                deleted_short_state := self.storage[hasher].set(
                    waiter_hash, short_state
                )
            ) is not None:
                await deleted_short_state.cancel()

            waiter_hashes[hasher] = waiter_hash

        async with lifespan:
            await event.wait()

        if short_state.context is None:
            raise LookupError("No context in short_state.")

        initiator = short_state.context.context.get(INITIATOR_CONTEXT_KEY)
        if initiator is None:
            raise LookupError("Initiator not found in short_state context.")

        for hasher, waiter_hash in waiter_hashes.items():
            self.storage[hasher].pop(waiter_hash, None)

        return (
            initiator,
            short_state.context.event,  # type: ignore
            *unpack(short_state.context.context),
        )

    async def clear_storage(self) -> None:
        """Clears storage."""

        for hasher in self.storage:
            now = datetime.datetime.now()
            for ident, short_state in self.storage.get(hasher, {}).copy().items():
                if (
                    short_state.expiration_date is not None
                    and now > short_state.expiration_date
                ):
                    await self.drop(hasher, data=ident, force=True)


async def clear_wm_storage_worker(
    wm: WaiterMachine,
    interval_seconds: int = 60,
) -> typing.NoReturn:
    while True:
        await wm.clear_storage()
        await asyncio.sleep(interval_seconds)


__all__ = ("WaiterMachine",)
