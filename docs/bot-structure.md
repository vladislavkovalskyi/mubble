# Bot Structure

This document explains the structure and components of a Mubble bot.

## Overview

The `Mubble` class (also aliased as `Bot`) is the central component of the framework. It coordinates the API client, dispatcher, polling mechanism, and other components to create a functioning bot.

## Basic Structure

A typical Mubble bot has the following structure:

```python
from mubble import API, Mubble, Token
from mubble.modules import logger

# Initialize components
api = API(token=Token("YOUR_BOT_TOKEN"))
bot = Mubble(api)

# Configure logging
logger.set_level("INFO")

# Register handlers
@bot.on.message(...)
async def handler(message):
    ...

# Run the bot
bot.run_forever()
```

## The Mubble Class

The `Mubble` class is the main entry point for creating a bot:

```python
class Mubble(Generic[HTTPClient, Dispatch, Polling, LoopWrapper]):
    def __init__(
        self,
        api: API[HTTPClient],
        *,
        dispatch: Dispatch | None = None,
        polling: Polling | None = None,
        loop_wrapper: LoopWrapper | None = None,
    ) -> None:
        ...
```

### Parameters

- `api`: An instance of the `API` class for communicating with the Telegram Bot API
- `dispatch`: An optional custom dispatcher (defaults to `Dispatch()`)
- `polling`: An optional custom polling mechanism (defaults to `Polling(api)`)
- `loop_wrapper`: An optional custom loop wrapper (defaults to `LoopWrapper()`)

## Components

### API Client

The API client handles communication with the Telegram Bot API:

```python
from mubble import API, Token

api = API(token=Token("YOUR_BOT_TOKEN"))
```

See [API Client](api-client.md) for more details.

### Dispatcher

The dispatcher routes incoming updates to the appropriate handlers based on rules. You interact with it through the `bot.on` property:

```python
@bot.on.message(...)  # Register a message handler
@bot.on.callback_query(...)  # Register a callback query handler
```

See [Dispatching](dispatching.md) for more details.

### Polling

The polling mechanism retrieves updates from the Telegram Bot API:

```python
from mubble.bot.polling import Polling

polling = Polling(api, timeout=30)
```

### Loop Wrapper

The loop wrapper manages the asyncio event loop:

```python
from mubble.tools.loop_wrapper import LoopWrapper

loop_wrapper = LoopWrapper()
```

## Running the Bot

There are two main ways to run a Mubble bot:

### Blocking Mode

The `run_forever()` method starts the bot in blocking mode:

```python
bot.run_forever()
```

This method blocks the current thread and runs the bot until it's interrupted.

### Non-Blocking Mode

You can also run the bot in non-blocking mode using `run_polling()`:

```python
async def main():
    await bot.run_polling()

# Run in an existing event loop
asyncio.run(main())
```

### Options

Both methods accept the following options:

- `offset`: The initial update offset (default: 0)
- `skip_updates`: Whether to skip pending updates (default: False)

```python
# Skip pending updates when starting
bot.run_forever(skip_updates=True)
```

## Customizing Components

You can customize the bot by providing your own implementations of its components:

```python
from mubble import API, Mubble, Token
from mubble.bot.dispatch import Dispatch
from mubble.bot.polling import Polling
from mubble.tools.loop_wrapper import LoopWrapper

# Create custom components
api = API(token=Token("YOUR_BOT_TOKEN"))
dispatch = Dispatch()  # Custom dispatcher
polling = Polling(api, timeout=60)  # Custom polling with longer timeout
loop_wrapper = LoopWrapper()  # Custom loop wrapper

# Create bot with custom components
bot = Mubble(
    api=api,
    dispatch=dispatch,
    polling=polling,
    loop_wrapper=loop_wrapper
)
```

## Error Handling

You can add error handling to your bot using the `ErrorHandler` class:

```python
from mubble import API, Mubble, Token
from mubble.tools.error_handler import ErrorHandler
from mubble.modules import logger

api = API(token=Token("YOUR_BOT_TOKEN"))
error_handler = ErrorHandler()

@error_handler.register
async def handle_error(error: Exception, event: Any) -> None:
    logger.error(f"Error processing event: {error}")

bot = Mubble(api)
bot.dispatch.error_handler = error_handler
```

## Middleware

You can add middleware to process updates before they reach handlers:

```python
from mubble import API, Mubble, Token, Update

api = API(token=Token("YOUR_BOT_TOKEN"))
bot = Mubble(api)

@bot.dispatch.middleware
async def middleware(update: Update, next_handler: Callable) -> Any:
    # Pre-processing
    print(f"Received update: {update.update_id}")
    
    # Call the next handler
    result = await next_handler(update)
    
    # Post-processing
    print(f"Processed update: {update.update_id}")
    
    return result
```

## Lifespan Management

You can use the `Lifespan` class to manage resources that need to be initialized and cleaned up:

```python
from mubble import API, Mubble, Token
from mubble.tools.lifespan import Lifespan

api = API(token=Token("YOUR_BOT_TOKEN"))
bot = Mubble(api)
lifespan = Lifespan()

@lifespan.on_startup
async def on_startup():
    print("Bot is starting up...")
    # Initialize resources

@lifespan.on_shutdown
async def on_shutdown():
    print("Bot is shutting down...")
    # Clean up resources

bot.loop_wrapper.lifespan = lifespan
bot.run_forever()
```

## Next Steps

Now that you understand the bot structure, you can explore:

- [Dispatching](dispatching.md)
- [Handlers](handlers.md)
- [Rules](rules.md)
- [Middleware](middleware.md) 