import inspect
import typing

from mubble.bot.dispatch.context import Context
from mubble.node.base import ComposeError
from mubble.node.composer import CONTEXT_STORE_NODES_KEY, Composition, NodeSession
from mubble.node.scope import NodeScope
from mubble.node.update import UpdateNode
from mubble.tools.magic import get_impls, impl


class Polymorphic:
    @classmethod
    async def compose(cls, update: UpdateNode, context: Context) -> typing.Any:
        scope = getattr(cls, "scope", None)
        node_ctx = context.get_or_set(CONTEXT_STORE_NODES_KEY, {})

        for i, impl in enumerate(get_impls(cls)):
            composition = Composition(impl, True)
            node_collection = await composition.compose_nodes(update, context)
            if node_collection is None:
                continue

            # To determine whether this is a right morph, all subnodes must be resolved
            if scope is NodeScope.PER_EVENT and (cls, i) in node_ctx:
                result: NodeSession = node_ctx[(cls, i)]
                await node_collection.close_all()
                return result.value

            result = composition.func(cls, **node_collection.values())
            if inspect.isawaitable(result):
                result = await result

            if scope is NodeScope.PER_EVENT:
                node_ctx[(cls, i)] = NodeSession(cls, result, {})

            await node_collection.close_all(with_value=result)
            return result

        raise ComposeError("No implementation found.")


__all__ = ("Polymorphic", "impl")
