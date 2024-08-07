import typing

from fntypes.result import Error, Ok, Result

from mubble.api.abc import ABCAPI
from mubble.bot.cute_types.update import UpdateCute
from mubble.bot.dispatch.context import Context
from mubble.bot.rules.adapter.abc import ABCAdapter, Event
from mubble.bot.rules.adapter.errors import AdapterError
from mubble.node.base import ComposeError
from mubble.node.composer import NodeSession, compose_node
from mubble.types.objects import Update

Ts = typing.TypeVarTuple("Ts")


class NodeAdapter(typing.Generic[*Ts], ABCAdapter[Update, Event[tuple[*Ts]]]):
    def __init__(self, *nodes: *Ts) -> None:
        self.nodes = nodes

    def __repr__(self) -> str:
        return "<{}: adapt Update -> {}>".format(
            self.__class__.__name__,
            Update.__name__,
            ", ".join(node.__name__ for node in self.nodes),
        )

    async def adapt(
        self, api: ABCAPI, update: Update
    ) -> Result[Event[tuple[*Ts]], AdapterError]:
        update_cute = UpdateCute.from_update(update, api)
        node_sessions: list[NodeSession] = []
        for node_t in self.nodes:
            try:
                # FIXME: adapters should have context
                node_sessions.append(
                    await compose_node(node_t, update_cute, Context(raw_update=update))
                )
            except ComposeError:
                for session in node_sessions:
                    await session.close(with_value=None)
                return Error(AdapterError(f"Couldn't compose nodes, error on {node_t}"))
        return Ok(Event(tuple(node_sessions)))


__all__ = ("NodeAdapter",)
