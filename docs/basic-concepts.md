# Basic Concepts

This document explains the fundamental concepts and components of the Mubble framework.

## Architecture Overview

Mubble follows a modular architecture with several key components:

1. **API Client**: Handles communication with the Telegram Bot API
2. **Bot**: The main class that coordinates all components
3. **Dispatch**: Routes incoming updates to appropriate handlers
4. **Handlers**: Functions that process specific types of updates
5. **Rules**: Conditions that determine when handlers should be executed
6. **Types**: Data structures representing Telegram API objects

## Core Components

### API Client

The API client is responsible for making HTTP requests to the Telegram Bot API. Mubble provides two client implementations:

- `AiohttpClient`: Default client based on aiohttp
- `AiosonicClient`: Alternative client based on aiosonic for potentially better performance

```python
from mubble import API, Token

# Create an API instance with the default client
api = API(token=Token("YOUR_BOT_TOKEN"))

# Or specify a client explicitly
from mubble.client import AiosonicClient
api = API(token=Token("YOUR_BOT_TOKEN"), client=AiosonicClient())
```

### Bot

The `Mubble` class (also aliased as `Bot`) is the central component that coordinates the API client, dispatcher, and polling mechanism:

```python
from mubble import API, Mubble, Token

api = API(token=Token("YOUR_BOT_TOKEN"))
bot = Mubble(api)

# Start the bot
bot.run_forever()
```

### Dispatch

The dispatcher routes incoming updates to the appropriate handlers based on rules. You typically interact with it through the `bot.on` property:

```python
@bot.on.message(...)  # Register a message handler
@bot.on.callback_query(...)  # Register a callback query handler
```

### Handlers

Handlers are asynchronous functions that process specific types of updates. They are registered with the dispatcher and executed when their associated rules match:

```python
@bot.on.message(Text("/start"))
async def start_handler(message: Message) -> None:
    await message.answer("Hello!")
```

### Rules

Rules are conditions that determine when handlers should be executed. Mubble provides many built-in rules:

```python
from mubble.rules import Text, Command, Regex

@bot.on.message(Text("/start"))  # Exact text match
@bot.on.message(Command("help"))  # Command match
@bot.on.message(Regex(r"^\d+$"))  # Regex pattern match
```

### Types

Mubble provides type-hinted classes for all Telegram API objects:

```python
from mubble import Message, User, Chat

async def handler(message: Message) -> None:
    user: User = message.from_user
    chat: Chat = message.chat
```

## Event Flow

1. The bot polls the Telegram API for updates
2. Updates are received and processed by the polling mechanism
3. Each update is passed to the dispatcher
4. The dispatcher checks each registered handler against its rules
5. If a rule matches, the corresponding handler is executed
6. The handler processes the update and may send responses

## Context and State Management

Mubble provides tools for managing context and state:

```python
from mubble import Context

@bot.on.message(...)
async def handler(message: Message, ctx: Context) -> None:
    # Store data in context
    ctx.set("user_id", message.from_user.id)
    
    # Retrieve data from context
    user_id = ctx.get("user_id")
```

## Error Handling

Mubble provides mechanisms for handling errors that occur during update processing:

```python
from mubble.tools.error_handler import ErrorHandler

error_handler = ErrorHandler()

@error_handler.register
async def handle_error(error: Exception, event: Any) -> None:
    logger.error(f"Error processing event: {error}")

bot = Mubble(api, error_handler=error_handler)
```

## Next Steps

Now that you understand the basic concepts, you can explore more specific topics:

- [API Client](api-client.md)
- [Bot Structure](bot-structure.md)
- [Dispatching](dispatching.md)
- [Handlers](handlers.md)
- [Rules](rules.md) 