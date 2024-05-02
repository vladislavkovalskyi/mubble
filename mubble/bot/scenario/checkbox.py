import dataclasses
import secrets
import typing

from mubble.bot.cute_types import CallbackQueryCute
from mubble.bot.dispatch.waiter_machine import WaiterMachine
from mubble.tools import InlineButton, InlineKeyboard
from mubble.tools.parse_mode import ParseMode
from mubble.types.objects import InlineKeyboardMarkup

from .abc import ABCScenario

if typing.TYPE_CHECKING:
    from mubble.api import API
    from mubble.bot.dispatch.view.abc import BaseStateView


@dataclasses.dataclass
class Choice:
    name: str
    is_picked: bool
    default_text: str
    picked_text: str
    code: str


class Checkbox(ABCScenario[CallbackQueryCute]):
    INVALID_CODE = "Invalid code"
    CALLBACK_ANSWER = "Done"
    PARSE_MODE = ParseMode.HTML

    def __init__(
        self,
        waiter_machine: WaiterMachine,
        chat_id: int,
        msg: str,
        *,
        ready_text: str = "Ready",
        max_in_row: int = 3,
    ) -> None:
        self.chat_id = chat_id
        self.msg = msg
        self.choices: list[Choice] = []
        self.ready = ready_text
        self.max_in_row = max_in_row
        self.random_code = secrets.token_hex(8)
        self.waiter_machine = waiter_machine
    
    def __repr__(self) -> str:
        return (
            "<{}@{!r}: (choices={!r}, max_in_row={}) with waiter_machine={!r}, ready_text={!r} "
            "for chat_id={} with message={!r}>"
        ).format(
            self.__class__.__name__,
            self.random_code,
            self.choices,
            self.max_in_row,
            self.waiter_machine,
            self.ready,
            self.chat_id,
            self.msg,
        )

    def get_markup(self) -> InlineKeyboardMarkup:
        kb = InlineKeyboard()
        choices = self.choices.copy()
        while choices:
            while len(kb.keyboard[-1]) < self.max_in_row and choices:
                choice = choices.pop(0)
                kb.add(
                    InlineButton(
                        text=choice.default_text
                        if not choice.is_picked
                        else choice.picked_text,
                        callback_data=self.random_code + "/" + choice.code,
                    )
                )
            kb.row()
        
        kb.add(InlineButton(self.ready, callback_data=self.random_code + "/ready"))
        return kb.get_markup()

    def add_option(
        self,
        name: str,
        default_text: str,
        picked_text: str,
        *,
        is_picked: bool = False,
    ) -> typing.Self:
        self.choices.append(
            Choice(name, is_picked, default_text, picked_text, secrets.token_hex(8)),
        )
        return self

    async def handle(self, cb: CallbackQueryCute) -> bool:
        code = cb.data.unwrap().replace(self.random_code + "/", "", 1)
        if code == "ready":
            return False

        for i, choice in enumerate(self.choices):
            if choice.code == code:
                # Toggle choice
                self.choices[i].is_picked = not self.choices[i].is_picked
                await cb.edit_text(
                    text=self.msg,
                    parse_mode=self.PARSE_MODE,
                    reply_markup=self.get_markup(),
                )
                break

        return True

    async def wait(
        self,
        api: "API",
        view: "BaseStateView[CallbackQueryCute]",
    ) -> tuple[dict[str, bool], int]:
        assert len(self.choices) > 1
        message = (
            await api.send_message(
                chat_id=self.chat_id,
                text=self.msg,
                parse_mode=self.PARSE_MODE,
                reply_markup=self.get_markup(),
            )
        ).unwrap()
        
        while True:
            q, _ = await self.waiter_machine.wait(view, (api, message.message_id))
            should_continue = await self.handle(q)
            await q.answer(self.CALLBACK_ANSWER)
            if not should_continue:
                break
        
        return (
            {choice.name: choice.is_picked for choice in self.choices},
            message.message_id,
        )


__all__ = ("Checkbox", "Choice")
