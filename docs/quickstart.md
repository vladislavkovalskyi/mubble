# Quick Start Guide

This guide will help you create your first Telegram bot with Mubble.

## Prerequisites

Before you begin, make sure you have:

1. Installed Mubble (see [Installation](installation.md))
2. Created a Telegram bot and obtained a token from [@BotFather](https://t.me/BotFather)

## Creating Your First Bot

Let's create a simple echo bot that responds to the `/start` command and echoes back any text messages it receives.

### 1. Set Up Your Project

Create a new directory for your project and create a file named `bot.py`:

```bash
mkdir my_first_bot
cd my_first_bot
touch bot.py
```

### 2. Write the Bot Code

Open `bot.py` in your favorite editor and add the following code:

```python
from mubble import API, Message, Mubble, Token
from mubble.modules import logger
from mubble.rules import StartCommand, Text

# Initialize the API with your bot token
api = API(token=Token("YOUR_BOT_TOKEN"))  # Replace with your actual token
# Or load from environment variable:
# api = API(token=Token.from_env())  # Set TOKEN environment variable

# Create a bot instance
bot = Mubble(api)

# Set logging level
logger.set_level("INFO")

# Handler for /start command
@bot.on.message(StartCommand())
async def start_handler(message: Message) -> None:
    await message.answer(f"Hello, {message.from_user.full_name}! I'm an echo bot created with Mubble.")

# Handler for any text message
@bot.on.message(Text())
async def echo_handler(message: Message) -> None:
    await message.answer(f"You said: {message.text}")

# Run the bot
if __name__ == "__main__":
    bot.run_forever()
```

### 3. Run Your Bot

Run your bot with:

```bash
python bot.py
```

### 4. Test Your Bot

Open Telegram and search for your bot by its username. Start a conversation and:

1. Send the `/start` command - the bot should greet you
2. Send any text message - the bot should echo it back

## Adding More Features

Let's enhance our bot with a few more features:

### Adding Command Handlers

```python
@bot.on.message(Text("/help"))
async def help_handler(message: Message) -> None:
    await message.answer(
        "This is a simple echo bot created with Mubble.\n"
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message"
    )
```

### Adding Inline Keyboards

```python
from mubble.tools.keyboard import InlineKeyboard, InlineButton
from mubble import CallbackQuery

@bot.on.message(Text("/menu"))
async def menu_handler(message: Message) -> None:
    keyboard = (
        InlineKeyboard()
        .add(InlineButton("Option 1", callback_data="option_1"))
        .add(InlineButton("Option 2", callback_data="option_2"))
    ).get_markup()
    
    await message.answer("Please select an option:", reply_markup=keyboard)

@bot.on.callback_query(lambda cq: cq.data == "option_1")
async def option_1_handler(callback_query: CallbackQuery) -> None:
    await callback_query.answer("You selected Option 1!")
    await callback_query.message.answer("You clicked Option 1")

@bot.on.callback_query(lambda cq: cq.data == "option_2")
async def option_2_handler(callback_query: CallbackQuery) -> None:
    await callback_query.answer("You selected Option 2!")
    await callback_query.message.answer("You clicked Option 2")
```

## Next Steps

Now that you've created your first bot, you can:

- Learn about [Basic Concepts](basic-concepts.md)
- Explore more [Examples](https://github.com/vladislavkovalskyi/mubble/blob/master/examples)
- Dive into the [API Client](api-client.md) documentation 