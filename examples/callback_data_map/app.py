from mubble import API, Message, Mubble, Token
from mubble.rules import CallbackDataMap, Text
from mubble.tools import InlineButton, InlineKeyboard

bot = Mubble(API(Token.from_env()))
keyboard = (
    InlineKeyboard()
    .add(InlineButton("Apple 🍏", callback_data={"item": "Apple", "amount": 10}))
    .add(InlineButton("Kiwi 🥝", callback_data={"item": "Kiwi", "amount": 15}))
    .add(InlineButton("Strawberry 🍓", callback_data={"item": "Strawberry", "amount": 20}))
).get_markup()


@bot.on.message(Text("/start"))
async def start(message: Message):
    await message.answer("🔥 Heyo! Choose smthing", reply_markup=keyboard)


@bot.on.callback_query(CallbackDataMap({"item": str, "amount": lambda v: v <= 20}))
async def eat_item(_, item: str, amount: int) -> str:
    return f"👌 U chose: {item} (x{amount})"


bot.run_forever()
