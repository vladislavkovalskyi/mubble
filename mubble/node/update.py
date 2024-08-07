from mubble.bot.cute_types import UpdateCute
from mubble.node.base import ScalarNode


class UpdateNode(ScalarNode, UpdateCute):
    @classmethod
    async def compose(cls, update: UpdateCute) -> UpdateCute:
        return update


__all__ = ("UpdateNode",)
