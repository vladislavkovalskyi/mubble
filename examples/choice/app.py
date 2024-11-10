from mubble import Token, API, Mubble, WaiterMachine, Message, Choice
from mubble.bot.dispatch.waiter_machine.hasher.callback import CALLBACK_QUERY_FOR_MESSAGE
from mubble.rules import Command
from mubble.modules import logger

api = API(token=Token.from_env())
bot = Mubble(api)
wm = WaiterMachine(bot.dispatch)

logger.set_level("INFO")


devices = {
    "iphone": ["📱 iPhone 15 Pro", 999.0],
    "ipad": ["📲 iPad Pro M4", 1299.0],
    "apple_watch": ["⌚️ Apple Watch Ultra 2", 799.0],
    "macbook": ["💻 Macbook Pro 16 M3 Pro", 2499.0],
}


@bot.on.message(Command("choice"))
async def action(message: Message):
    chosen, message_id = await (
        Choice(
            wm,
            message.chat.id,
            "Pick one of these devices.",
            ready_text="Pick!",
            cancel_text="Cancel",
            max_in_row=2,
        )
        .add_option("iphone", "iPhone", "iPhone 🟢", is_picked=True)
        .add_option("ipad", "iPad", "iPad 🟢")
        .add_option("apple_watch", "Apple watch", "Apple watch 🟢")
        .add_option("macbook", "Macbook", "Macbook 🟢")
        .wait(CALLBACK_QUERY_FOR_MESSAGE, message.ctx_api, bot.dispatch.callback_query)
    )

    name, price = devices[chosen]
    await message.edit(
        text=f"You've picked the {name}, which goes for {price:.2f} bucks.",
        message_id=message_id,
    )


bot.run_forever()
