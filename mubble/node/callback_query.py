from mubble.bot.cute_types import CallbackQueryCute
from mubble.node.base import ComposeError, ScalarNode
from mubble.node.update import UpdateNode


class CallbackQueryNode(ScalarNode, CallbackQueryCute):
    @classmethod
    async def compose(cls, update: UpdateNode) -> CallbackQueryCute:
        if not update.callback_query:
            raise ComposeError
        return CallbackQueryCute(
            **update.callback_query.unwrap().to_dict(),
            api=update.api,
        )


__all__ = ("CallbackQueryNode",)
