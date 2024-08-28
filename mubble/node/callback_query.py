from mubble.bot.cute_types.callback_query import CallbackQueryCute
from mubble.node.base import ComposeError, ScalarNode
from mubble.node.update import UpdateNode


class CallbackQueryNode(ScalarNode, CallbackQueryCute):
    @classmethod
    async def compose(cls, update: UpdateNode) -> CallbackQueryCute:
        if not update.callback_query:
            raise ComposeError("Update is not a callback_query.")
        return update.callback_query.unwrap()


__all__ = ("CallbackQueryNode",)
