import dataclasses

from mubble import (
    API,
    CallbackQuery,
    InlineButton,
    InlineKeyboard,
    Message,
    Mubble,
    Token,
)
from mubble.modules import logger
from mubble.node.payload import PayloadData
from mubble.rules import (
    StartCommand,
    PayloadEqRule,
    PayloadMarkupRule,
    PayloadModelRule,
)
from mubble.tools import MsgPackSerializer

api = API(token=Token.from_env())
bot = Mubble(api)
logger.set_level("DEBUG")


@dataclasses.dataclass(slots=True, frozen=True)
class Item:
    __key__ = "item"

    name: str
    amount: int = dataclasses.field(kw_only=True)


item_serializer = MsgPackSerializer(Item)
kb = (
    InlineKeyboard()
    .add(InlineButton("Confirm", callback_data="confirm/action"))
    .row()
    .add(InlineButton("One", callback_data="number/1"))
    .add(InlineButton("Two", callback_data="number/2"))
    .row()
    .add(
        InlineButton(
            "🍎",
            callback_data=Item("apple", amount=5),
            callback_data_serializer=item_serializer,
        )
    )
    .add(
        InlineButton(
            "🥝",
            callback_data=Item("kiwi", amount=10),
            callback_data_serializer=item_serializer,
        ),
    )
    .row()
).get_markup()


@bot.on.message(StartCommand())
async def start(m: Message):
    await m.answer("🔥 Please confirm doing action.", reply_markup=kb)


@bot.on.callback_query(is_blocking=False)
async def handle_fruit_item(item: PayloadData[Item, MsgPackSerializer[Item]]):
    logger.info("Got fruit item={!r}", item)


@bot.on.callback_query(PayloadEqRule("confirm/action"))
async def confirm_handler(cb: CallbackQuery):
    await cb.answer("Okay! Confirmed.")
    await cb.edit_text(text="Action happens.")


@bot.on.callback_query(PayloadMarkupRule("number/<n:int>"))
async def number_handler(cb: CallbackQuery, n: int):
    await cb.answer(f"🤬 It's fruit #{n}!")


@bot.on.callback_query(
    PayloadModelRule(Item, serializer=MsgPackSerializer, alias="item")
)
async def select_item(cb: CallbackQuery, item: Item):
    await cb.answer(f"You took {item.name!r} for {item.amount} bucks!")


bot.run_forever()
