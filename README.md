# Mubble 1.3.0 (stable)

[![Downloads](https://img.shields.io/pypi/dm/mubble.svg?style=flat-square)](https://pypi.python.org/pypi/mubble)
[![Downloads](https://img.shields.io/pypi/pyversions/mubble.svg?style=flat-square)](https://pypi.python.org/pypi/mubble)

<a href="https://github.com/vladislavkovalskyi/mubble">
  <img src="https://github.com/vladislavkovalskyi/mubble/blob/master/images/mubble_logo.png?raw=true" alt="Github" width="100%">
</a>

<a href="https://github.com/vladislavkovalskyi/mubble/blob/master/examples">
  <img src="https://github.com/vladislavkovalskyi/mubble/blob/master/images/click_here.png?raw=true" alt="Examples" width="100%">
</a>

<br>

**Mubble** is a next-generation framework known for its great speed and simplicity. It is written using aiohttp, asyncio, and msgspec.<br>
*([Author](https://github.com/vladislavkovalskyi)'s words)*
**Make the fastest bot ever!**

<br>

# Speed measurement
Each test contains **100 different API calls**

| Test    | Mubble (sec/avg)  | Aiogram (sec/avg) | Telebot (sec/avg) | Winner     |
|---------|-------------------|-------------------|-------------------|------------|
| 1       | **0.12896**       | 0.30656           | 0.24000           | Mubble     |
| 2       | **0.12620**       | 0.14554           | 0.17649           | Mubble     |
| 3       | **0.13366**       | 0.14902           | 0.13141           | Mubble     |
| 4       | **0.12437**       | 0.14864           | 0.13717           | Mubble     |
| 5       | **0.12754**       | 0.15863           | 0.18894           | Mubble     |
| 6       | **0.12261**       | 0.15175           | 0.17157           | Mubble     |
| 7       | **0.14395**       | 0.16154           | 0.19383           | Mubble     |
| 8       | **0.12508**       | 0.15084           | 0.24207           | Mubble     |
| 9       | **0.12239**       | 0.14838           | 0.14282           | Mubble     |
| 10      | **0.12610**       | 0.14478           | 0.13068           | Mubble     |
|         |                   |                   |                   |            |
| **AVG** | **0.12869**       | 0.16687           | 0.17550           | **Mubble** |

<br>

# Getting started

### Installing:
```bash
pip install mubble
```

```bash
poetry add mubble
```

```bash
poetry add git+https://github.com/vladislavkovalskyi/mubble.git#master
```

### Simple bot example:
```python
import random

from mubble import Token, API, Mubble, Message, CallbackQuery
from mubble.rules import StartCommand, Text, Markup, CallbackData
from mubble.tools.keyboard import InlineKeyboard, InlineButton

api = API(Token("Your token"))
bot = Mubble(api)


class Keyboard:
    menu = (
        InlineKeyboard()
        .add(InlineButton("✍️ Write hello", callback_data="hello"))
        .row()
        .add(InlineButton("🍌 Choice banana", callback_data="banana"))
    ).get_markup()

    back = (
        InlineKeyboard().add(InlineButton("⬅️ Back", callback_data="menu"))
    ).get_markup()


@bot.on.message(StartCommand())
async def start_handler(message: Message):
    await message.answer(
        "👋 Hello, I'm Mubble! How can I help you?\n\n"
        "My available commands:\n"
        "- /start\n"
        "- /menu\n"
        "- /random [from number] [to number]"
    )


@bot.on.message(Text("/menu"))
async def menu_handler(message: Message):
    await message.answer(
        "📃 Here's your menu! Use the keyboard.", reply_markup=Keyboard.menu
    )


@bot.on.message(Markup(["/random", "/random <a:int> <b:int>"]))
async def random_handler(message: Message, a: int = None, b: int = None):
    if None in (a, b):
        await message.answer(
            "🤓 Wrong syntax. You also need to write the first number and the second number."
        )
        return

    await message.answer(f"🎲 Your random number is {random.randint(a, b)}")


@bot.on.callback_query(CallbackData("menu"))
async def menu_handler(cq: CallbackQuery):
    await cq.edit_text(
        "📃 Here's your menu! Use the keyboard.", reply_markup=Keyboard.menu
    )


@bot.on.callback_query(CallbackData("hello"))
async def hello_handler(cq: CallbackQuery):
    await cq.edit_text("👋 Hello, I'm Mubble!", reply_markup=Keyboard.back)


@bot.on.callback_query(CallbackData("banana"))
async def fruits_handler(cq: CallbackQuery):
    await cq.answer("You clicked on the 🍌!")


bot.run_forever()
```

Слава Україні! 🇺🇦


*by Vladyslav Kovalskyi*
