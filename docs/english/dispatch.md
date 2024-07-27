<img src="../../images/mubble_logo.png" alt="Mubble logo" width="50%" height="50%">

# Dispatch (English 🇬🇧)
This example is created to demonstrate how to work with **Dispatch** in **Mubble**.

**Why do you need Dispatch?**<br>
You will need it when you want to create a good structure for your bot and separate all handlers into different files/folders.

## Code Example

### File: `project/app.py`
In this example, we follow the standard initialization scheme for our bot, but before that, we initialize our `Dispatch` class, in which we will load other instances from files, which in our case are located in the commands directory.
```python
from mubble import Dispatch, Token, API, Mubble

from commands import start, info

dispatch = Dispatch()
for b in (start, info):
    dispatch.load(b.dispatch)

api = API(Token.from_env())
bot = Mubble(api, dispatch=dispatch)

bot.run_forever()
```

### File: `project/commands/start.py`
In this case, we initialize our `Dispatcher`. Its feature is that you can use it just like `@bot`.

```python
from mubble import Dispatch, Message
from mubble.rules import StartCommand

dispatch = Dispatch()


@dispatch.message(StartCommand())
async def start(message: Message):
    await message.answer("😉 Hello! This is a start message.")
```

### File: `project/commands/info.py`
In this case, we initialize our `Dispatcher`. Its feature is that you can use it just like `@bot`.
```python
from mubble import Dispatch, Message
from mubble.rules import Text

dispatch = Dispatch()


@dispatch.message(Text("/info"))
async def info(message: Message):
    await message.answer(
        f"🐥 Info about you:\n"
        f"- Telegram ID: {message.from_user.id}\n"
        f"- Name: {message.from_user.first_name}\n"
        f"- Premium: {'yes' if message.from_user.is_premium else 'no'}"
    )
```

### File: `project/commands/__init__.py`
In the `__init__.py` file, we import our files so that we can later import our files from the commands folder without any issues.
```python
from . import start, info

__all__ = ["start", "info"]
```

## Example of use
<img src="../../images/dispatcher.jpg" alt="Mubble dispatcher" width="50%" height="50%">
