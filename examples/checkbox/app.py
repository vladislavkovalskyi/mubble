from mubble import API, Checkbox, Message, Mubble, Token, WaiterMachine
from mubble.bot.dispatch.waiter_machine.hasher.callback import CALLBACK_QUERY_FOR_MESSAGE
from mubble.rules import Command

api = API(token=Token.from_env())
bot = Mubble(api)
wm = WaiterMachine(bot.dispatch)


@bot.on.message(Command("checkbox"))
async def action(message: Message):
    picked, message_id = await (
        Checkbox(
            wm,
            message.chat.id,
            "Pick the fruits you vibe with!",
            ready_text="✅ Done!",
            cancel_text="❌ Cancel",
            max_in_row=2,
        )
        .add_option("apple", "🍏", "Apple")
        .add_option("kiwi", "🥝", "Kiwi", is_picked=True)
        .add_option("strawberry", "🍓", "Strawberry")
        .add_option("orange", "🍊", "Orange", is_picked=True)
        .add_option("peach", "🍑", "Peach")
        .wait(CALLBACK_QUERY_FOR_MESSAGE, message.ctx_api, bot.dispatch.callback_query)
    )

    await message.edit(
        text=f"You picked: {", ".join(name for name in picked if picked[name])}",
        chat_id=message.chat.id,
        message_id=message_id,
    )

bot.run_forever()
