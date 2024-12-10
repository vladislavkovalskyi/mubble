import typing

from mubble.bot.dispatch.context import Context
from mubble.node.base import Node
from mubble.tools.adapter.node import NodeAdapter

from .abc import ABCRule


class NodeRule(ABCRule[tuple[Node, ...]]):
    def __init__(self, *nodes: type[Node] | tuple[str, type[Node]]) -> None:
        bindings = [
            binding if isinstance(binding, tuple) else (None, binding)
            for binding in nodes
        ]
        self.nodes = [binding[1] for binding in bindings]
        self.node_keys = [binding[0] for binding in bindings]

    @property
    def adapter(self) -> NodeAdapter:
        return NodeAdapter(*self.nodes)  # type: ignore

    def check(
        self, resolved_nodes: tuple[Node, ...], ctx: Context
    ) -> typing.Literal[True]:
        for i, node in enumerate(resolved_nodes):
            if key := self.node_keys[i]:
                ctx[key] = node
        return True


__all__ = ("NodeRule",)
