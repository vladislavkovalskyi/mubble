# Mubble
Feature-rich telegram framework.

# Getting started

Installing:
```
pip install mubble
```

Example:
```python
from mubble import Mubble, API, Token, Message
from mubble.rules import Text
import logging

api = API(token=Token("123:abc"))
bot = Mubble(api)
logging.basicConfig(level=logging.INFO)

@bot.on.message(Text("/start"))
async def start_handler(message: Message):
    await message.answer(f"Hi, {message.from_.first_name}!")

bot.run_forever()
```
