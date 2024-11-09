import pathlib

from mubble_old import Token, API, Mubble, Message
from mubble_old.modules import logger
from mubble_old.rules import Command
from mubble_old.types import InputFile

api = API(token=Token.from_env())
bot = Mubble(api)
logger.set_level("INFO")

mubble_logo = pathlib.Path("images/mubble_logo.png").read_bytes()


@bot.on.message(Command("photo"))
async def start(message: Message):
    await message.answer_photo(
        InputFile("mubble.png", mubble_logo),
        caption="📸 Here's a pic for you!",
    )


bot.run_forever()
