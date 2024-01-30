<img src="../../images/mubble_logo.png" alt="Mubble logo" width="50%" height="50%">

# Image (Ukrainian 🇺🇦)
This example is created to demonstrate how to work with **files** in **Mubble**.

* `pathlib`, specifically the `Path` class, will help you specify the path to your image and retrieve its bytes, allowing you to save them to the `mubble_image` variable _(for example)_.
* Next, we call the `Telegram API method` called `send_photo`, which allows sending images. The main parameter is `chat_id`, which needs to be passed so that the bot knows which chat to send messages to, and `photo` takes two objects: `file name and format` and `the image itself in bytes` (`filename`, `bytes`).

## Example code for sending an image
```python
from mubble import Token, API, Mubble, Message
from mubble.rules import Text

from pathlib import Path

api = API(Token("Your token"))
bot = Mubble(api)

mubble_image = Path("mubble.png").read_bytes()

@bot.on.message(Text("/image"))
async def image(message: Message):
    await api.send_photo(
        chat_id=message.chat.id,
        photo=("image.png", mubble_image),
    )

bot.run_forever()
