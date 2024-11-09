from mubble.api.api import API
from mubble.bot.cute_types import UpdateCute
from mubble.node.base import ScalarNode
from mubble.types.objects import Update


class UpdateNode(ScalarNode, UpdateCute):
    @classmethod
    def compose(cls, update: Update, api: API) -> UpdateCute:
        if isinstance(update, UpdateCute):
            return update
        return UpdateCute.from_update(update, api)


__all__ = ("UpdateNode",)
