import abc
import typing

from mubble.bot.cute_types import ChatJoinRequestCute
from mubble.bot.dispatch.context import Context
from mubble.bot.rules.adapter import EventAdapter
from mubble.types.enums import UpdateType

from .abc import ABCRule

ChatJoinRequest: typing.TypeAlias = ChatJoinRequestCute


class ChatJoinRequestRule(ABCRule[ChatJoinRequest], requires=[]):
    adapter: EventAdapter[ChatJoinRequest] = EventAdapter(UpdateType.CHAT_JOIN_REQUEST, ChatJoinRequest)

    @abc.abstractmethod
    async def check(self, event: ChatJoinRequest, ctx: Context) -> bool:
        pass


class HasInviteLink(ChatJoinRequestRule):
    async def check(self, event: ChatJoinRequest, ctx: Context) -> bool:
        return bool(event.invite_link)


class InviteLinkName(ChatJoinRequestRule, requires=[HasInviteLink()]):
    def __init__(self, name: str, /) -> None:
        self.name = name

    async def check(self, event: ChatJoinRequest, ctx: Context) -> bool:
        return event.invite_link.unwrap().name.unwrap_or_none() == self.name


class InviteLinkByCreator(ChatJoinRequestRule, requires=[HasInviteLink()]):
    def __init__(self, creator_id: int, /) -> None:
        self.creator_id = creator_id

    async def check(self, event: ChatJoinRequest, ctx: Context) -> bool:
        return event.invite_link.unwrap().creator.id == self.creator_id


__all__ = (
    "ChatJoinRequestRule",
    "HasInviteLink",
    "InviteLinkByCreator",
    "InviteLinkName",
)
