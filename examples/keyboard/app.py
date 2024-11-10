from msgspec import Struct

from mubble import (
    API,
    CallbackQuery,
    InlineButton,
    InlineKeyboard,
    Message,
    Mubble,
    Token,
)
from mubble.rules import PayloadModelRule, Text
from mubble.tools.parse_mode import ParseMode

api = API(token=Token.from_env())
api.default_params["parse_mode"] = ParseMode.HTML
bot = Mubble(api)


# Alternative: use @dataclasses.dataclass decorator
class ItemModel(Struct):
    item: str
    price: float
    action: str


keyboard = (
    InlineKeyboard()
    .add(
        InlineButton(
            text="Kiwi",
            callback_data=ItemModel(item="kiwi", price=49.99, action="buy"),
        )
    )
    .add(
        InlineButton(
            text="Strawberry",
            callback_data=ItemModel(item="strawberry", price=24.49, action="buy"),
        )
    )
).get_markup()


@bot.on.message(Text("/start"))
async def start(message: Message):
    await message.answer(
        text=(
            "🔥 Hey! What do u want?\n"
            "<blockquote>"
            "- Kiwi costs <b>$49.99</b>\n"
            "- Strawberry costs <b>$24.49</b>"
            "</blockquote>"
        ),
        reply_markup=keyboard,
    )


@bot.on.callback_query(PayloadModelRule(ItemModel))
async def buy(cq: CallbackQuery, model: ItemModel):
    await cq.edit_text(
        f"🎁 You bought a <b>{model.item}</b> for <b>${model.price:.2f}</b>."
    )


bot.run_forever()
