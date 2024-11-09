from mubble.bot.cute_types.message import MessageCute
from mubble.node.base import ComposeError, ScalarNode
from mubble.node.update import UpdateNode


class MessageNode(ScalarNode, MessageCute):
    @classmethod
    def compose(cls, update: UpdateNode) -> MessageCute:
        if not update.message:
            raise ComposeError("Update is not a message.")
        return update.message.unwrap()


__all__ = ("MessageNode",)
