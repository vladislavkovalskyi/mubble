import typing_extensions as typing
from fntypes.result import Error, Ok, Result

from mubble.api.api import API
from mubble.bot.dispatch.context import Context
from mubble.bot.rules.adapter.abc import ABCAdapter, Event
from mubble.bot.rules.adapter.errors import AdapterError
from mubble.msgspec_utils import repr_type
from mubble.node.composer import NodeSession, compose_nodes
from mubble.types.objects import Update

if typing.TYPE_CHECKING:
    from mubble.node.base import Node


class NodeAdapter[*Nodes](ABCAdapter[Update, Event[tuple[*Nodes]]]):
    def __init__(self, *nodes: *Nodes) -> None:
        self.nodes = nodes

    def __repr__(self) -> str:
        return "<{}: adapt Update -> ({})>".format(
            self.__class__.__name__,
            ", ".join(repr_type(node) for node in self.nodes),
        )

    async def adapt(
        self,
        api: API,
        update: Update,
        context: Context,
    ) -> Result[Event[tuple[*Nodes]], AdapterError]:
        result = await compose_nodes(
            nodes={str(i): typing.cast(type["Node"], node) for i, node in enumerate(self.nodes)},
            ctx=context,
            data={Update: update, API: api},
        )

        match result:
            case Ok(collection):
                sessions: list[NodeSession] = list(collection.sessions.values())
                return Ok(Event(tuple(sessions)))  # type: ignore
            case Error(err):
                return Error(AdapterError(f"Couldn't compose nodes, error: {err}."))


__all__ = ("NodeAdapter",)
