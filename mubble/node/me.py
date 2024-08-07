from mubble.api.api import API
from mubble.types import User

from .base import ComposeError, ScalarNode
from .scope import GLOBAL


class Me(ScalarNode, User):
    scope = GLOBAL

    @classmethod
    async def compose(cls, api: API) -> User:
        me = await api.get_me()
        return me.expect(ComposeError("Can't complete get_me request"))


__all__ = ("Me",)
