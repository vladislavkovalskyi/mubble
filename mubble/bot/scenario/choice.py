import typing

from mubble.bot.cute_types.callback_query import CallbackQueryCute
from mubble.bot.dispatch.waiter_machine.hasher.hasher import Hasher
from mubble.bot.scenario.checkbox import Checkbox, ChoiceCode

if typing.TYPE_CHECKING:
    from mubble.api.api import API
    from mubble.bot.dispatch.view.base import BaseStateView

    class Choice[Key: typing.Hashable](Checkbox[Key]):
        async def wait(
            self,
            hasher: Hasher[CallbackQueryCute, int],
            api: API,
            view: BaseStateView[CallbackQueryCute],
        ) -> tuple[Key, int]: ...

else:

    class Choice(Checkbox):
        async def handle(self, cb):
            code = cb.data.unwrap().replace(self.random_code + "/", "", 1)
            if code == ChoiceCode.READY:
                return False

            for choice in self.choices:
                choice.is_picked = False

            for i, choice in enumerate(self.choices):
                if choice.code == code:
                    self.choices[i].is_picked = True
                    await cb.ctx_api.edit_message_text(
                        text=self.message,
                        chat_id=cb.message.unwrap().v.chat.id,
                        message_id=cb.message.unwrap().v.message_id,
                        parse_mode=self.PARSE_MODE,
                        reply_markup=self.get_markup(),
                    )

            return True

        async def wait(self, hasher, api, view):
            if len(tuple(choice for choice in self.choices if choice.is_picked)) != 1:
                raise ValueError("Exactly one choice must be picked")
            choices, m_id = await super().wait(hasher, api, view)
            return tuple(choices.keys())[tuple(choices.values()).index(True)], m_id


__all__ = ("Choice",)
