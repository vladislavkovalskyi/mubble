import pathlib

from mubble import API, Message, Mubble, Token
from mubble.bot.dispatch.context import Context
from mubble.rules import MessageRule

bot = Mubble(API(Token.from_env()))
photos_path = pathlib.Path("photos")
photos_path.mkdir(exist_ok=True)


class HasPhoto(MessageRule):
    async def check(self, message: Message, ctx: Context) -> bool:
        return bool(message.photo and message.photo.unwrap())


@bot.on.message(HasPhoto())
async def downloader(message: Message) -> str:
    photo_id = message.photo.unwrap()[-1].file_id
    photo_obj = (await message.ctx_api.get_file(file_id=photo_id)).unwrap()
    photo_path = photo_obj.file_path.unwrap()
    photo_bytes: bytes = await message.ctx_api.download_file(photo_path)

    path = photos_path / pathlib.Path(photo_path.split("/")[-1])
    path.write_bytes(photo_bytes)
    await message.answer(f"📸 Photo saved to {path}")


bot.run_forever()
