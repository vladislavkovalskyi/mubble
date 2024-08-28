from mubble.api.api import API
from mubble.node.base import ComposeError, ScalarNode
from mubble.node.scope import GLOBAL
from mubble.types.objects import User


class Me(ScalarNode, User):
    scope = GLOBAL

    @classmethod
    async def compose(cls, api: API) -> User:
        me = await api.get_me()
        return me.expect(ComposeError("Can't complete get_me request"))


__all__ = ("Me",)
