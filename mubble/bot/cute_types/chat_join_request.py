import typing

from fntypes.result import Result

from mubble.api.abc import ABCAPI, APIError
from mubble.types.objects import ChatJoinRequest, User

from .base import BaseCute, shortcut
from .chat_member_updated import ChatMemberShortcuts, chat_member_interaction


class ChatJoinRequestCute(BaseCute[ChatJoinRequest], ChatJoinRequest, ChatMemberShortcuts, kw_only=True):
    api: ABCAPI

    @property
    def from_user(self) -> User:
        return self.from_

    @property
    def user_id(self) -> int:
        return self.from_user.id

    @shortcut("approve_chat_join_request", executor=chat_member_interaction)
    async def approve(
        self,
        chat_id: int | str | None = None,
        user_id: int | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Shortcut `API.approve_chat_join_request()`, see the [documentation](https://core.telegram.org/bots/api#approvechatjoinrequest)

        Use this method to approve a chat join request. The bot must be an administrator
        in the chat for this to work and must have the can_invite_users administrator
        right. Returns True on success.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param user_id: Unique identifier of the target user.
        """

        ...

    @shortcut("decline_chat_join_request", executor=chat_member_interaction)
    async def decline(
        self,
        chat_id: int | str | None = None,
        user_id: int | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Shortcut `API.decline_chat_join_request()`, see the [documentation](https://core.telegram.org/bots/api#declinechatjoinrequest)

        Use this method to decline a chat join request. The bot must be an administrator
        in the chat for this to work and must have the can_invite_users administrator
        right. Returns True on success.

        :param chat_id: Unique identifier for the target chat or username of the target channel \
        (in the format @channelusername).

        :param user_id: Unique identifier of the target user.
        """

        ...


__all__ = ("ChatJoinRequestCute",)
