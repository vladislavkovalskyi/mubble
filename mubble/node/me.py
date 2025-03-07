from mubble.api.api import API
from mubble.node.base import ComposeError, scalar_node
from mubble.node.scope import GLOBAL
from mubble.types.objects import User


@scalar_node(scope=GLOBAL)
class Me:
    @classmethod
    async def compose(cls, api: API) -> User:
        me = await api.get_me()
        return me.expect(ComposeError("Can't complete api.get_me() request."))


__all__ = ("Me",)
