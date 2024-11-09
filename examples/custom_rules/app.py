from mubble_old import InlineButton, InlineKeyboard, Token, API, Mubble, Message
from mubble_old.bot.dispatch.context import Context
from mubble_old.bot.rules.callback_data import CallbackQuery
from mubble_old.rules import MessageRule, CallbackQueryRule, Command, CallbackData
from mubble_old.modules import logger

api = API(Token.from_env())
bot = Mubble(api)

logger.set_level("INFO")
OWNER_ID = 1734816882  # Use your Telegram id

keyboard = (
    InlineKeyboard().add(InlineButton("👋🏼 Bye!", callback_data="bye"))
).get_markup()


class HasPhoto(MessageRule):
    async def check(self, message: Message, ctx: Context) -> bool:
        return bool(message.photo and message.photo.unwrap())


class IsOwnerMessage(MessageRule):
    async def check(self, message: Message, ctx: Context) -> bool:
        return message.from_user.id == OWNER_ID


class IsOwnerCallback(CallbackQueryRule):
    async def check(self, event: CallbackQuery, ctx: Context) -> bool:
        return event.from_user.id == OWNER_ID


@bot.on.message(HasPhoto())
async def photo_handler(message: Message):
    await message.answer("📸 Looks like you just dropped a pic.")


@bot.on.message(Command("hello") & IsOwnerMessage())
async def owner_hello_handler(message: Message):
    await message.answer("🥳 Hi, owner!", reply_markup=keyboard)


@bot.on.message(Command("hello"))
async def hello_handler(message: Message):
    await message.answer("🥳 Hi, user!", reply_markup=keyboard)


@bot.on.callback_query(CallbackData("bye") & IsOwnerCallback())
async def owner_bye_handler(cq: CallbackQuery):
    await cq.edit_text("👋🏼 Bye, owner!")


@bot.on.callback_query(CallbackData("bye"))
async def bye_handler(cq: CallbackQuery):
    await cq.edit_text("👋🏼 Bye, user!")


bot.run_forever()
