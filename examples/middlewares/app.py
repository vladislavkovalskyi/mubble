from mubble_old import (
    API,
    ABCMiddleware,
    CallbackQuery,
    InlineButton,
    InlineKeyboard,
    Message,
    Mubble,
    ParseMode,
    Token,
)
from mubble_old.bot import Context
from mubble_old.bot.rules.callback_data import CallbackData
from mubble_old.modules import logger
from mubble_old.rules import Command
from mubble_old.tools import GlobalContext

api = API(token=Token.from_env())
bot = Mubble(api)
global_ctx = GlobalContext(msg_counter=dict(), cb_counter=dict())

logger.set_level("INFO")

keyboard = (
    InlineKeyboard()
    .add(InlineButton("🍪 Click", callback_data="click"))
    .row()
    .add(InlineButton("👉🏼 Clicks count", callback_data="count"))
).get_markup()


@bot.on.message.register_middleware()
class MessageContextMiddleware(ABCMiddleware[Message]):
    async def pre(self, event: Message, ctx: Context) -> bool:
        counter = global_ctx.get_value("msg_counter", dict[int, int]).unwrap()
        counter[event.from_user.id] = counter.get(event.from_user.id, 0) + 1

        ctx.set("msg_count", counter[event.from_user.id])
        return True


@bot.on.callback_query.register_middleware()
class CallbackContextMiddleware(ABCMiddleware[CallbackQuery]):
    async def pre(self, event: CallbackQuery, ctx: Context) -> bool:
        counter = global_ctx.get_value("cb_counter", dict[int, int]).unwrap()
        counter[event.from_user.id] = counter.get(event.from_user.id, 0) + 1

        ctx.set("cb_count", counter[event.from_user.id])
        return True


@bot.on.message(Command("count"))
async def count_handler(message: Message, msg_count: int):
    await message.answer(
        f"💬 <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>, you've sent {msg_count} messages!",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard,
    )


@bot.on.callback_query(CallbackData("click"))
async def click_handler(cq: CallbackQuery, cb_count: int):
    await cq.answer(f"Total: {cb_count} clicks")


@bot.on.callback_query(CallbackData("count"))
async def clicks_count_handler(cq: CallbackQuery, cb_count: int):
    await cq.answer()
    await cq.edit_text(
        f"💬 <a href='tg://user?id={cq.from_user.id}'>{cq.from_user.first_name}</a>, you've clicked the buttons {cb_count} times!",
        parse_mode=ParseMode.HTML,
    )


bot.run_forever()
