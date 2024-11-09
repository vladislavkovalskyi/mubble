from mubble.bot.cute_types.pre_checkout_query import PreCheckoutQueryCute
from mubble.node.base import ScalarNode
from mubble.node.update import UpdateNode


class PreCheckoutQueryNode(ScalarNode, PreCheckoutQueryCute):
    @classmethod
    def compose(cls, update: UpdateNode) -> PreCheckoutQueryCute:
        return update.pre_checkout_query.expect("Update is not a pre_checkout_query.")


__all__ = ("PreCheckoutQueryNode",)
