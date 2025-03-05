# Dispatching

This document explains how the dispatching system works in Mubble and how to use it effectively.

## Overview

The dispatcher is a core component of Mubble that routes incoming updates to the appropriate handlers based on rules. It's responsible for:

1. Receiving updates from the polling mechanism
2. Checking each update against registered handlers
3. Executing matching handlers
4. Managing the flow of updates through middleware

## Basic Usage

You typically interact with the dispatcher through the `bot.on` property:

```python
from mubble import API, Message, Mubble, Token
from mubble.rules import Text

api = API(token=Token("YOUR_BOT_TOKEN"))
bot = Mubble(api)

# Register a handler with the dispatcher
@bot.on.message(Text("/start"))
async def start_handler(message: Message) -> None:
    await message.answer("Hello!")

bot.run_forever()
```

## Dispatch Class

The `Dispatch` class is the main implementation of the dispatcher:

```python
from mubble.bot.dispatch import Dispatch

# Create a custom dispatcher
dispatch = Dispatch()

# Register a handler
@dispatch.message(Text("/start"))
async def start_handler(message: Message) -> None:
    await message.answer("Hello!")

# Create a bot with the custom dispatcher
bot = Mubble(api, dispatch=dispatch)
```

## Handler Registration

The dispatcher provides methods for registering handlers for different types of updates:

### Message Handlers

```python
@bot.on.message(Text("/start"))
async def start_handler(message: Message) -> None:
    await message.answer("Hello!")
```

### Callback Query Handlers

```python
@bot.on.callback_query(lambda cq: cq.data == "option_1")
async def option_1_handler(callback_query: CallbackQuery) -> None:
    await callback_query.answer("You selected Option 1!")
```

### Inline Query Handlers

```python
@bot.on.inline_query()
async def inline_handler(inline_query: InlineQuery) -> None:
    # Handle inline query
    ...
```

### Chat Join Request Handlers

```python
@bot.on.chat_join_request()
async def join_request_handler(join_request: ChatJoinRequest) -> None:
    await join_request.approve()
```

### Raw Update Handlers

```python
@bot.on.raw_update()
async def raw_update_handler(update: Update) -> None:
    # Handle any type of update
    ...
```

## Handler Priority

You can specify the priority of handlers to control the order in which they are checked:

```python
@bot.on.message(Text("/start"), priority=10)
async def high_priority_handler(message: Message) -> None:
    # This handler will be checked before lower priority handlers
    ...

@bot.on.message(Text("/start"), priority=1)
async def low_priority_handler(message: Message) -> None:
    # This handler will only be executed if higher priority handlers don't match
    ...
```

Higher priority values mean the handler will be checked earlier.

## Handler Finality

By default, if a handler is executed, no other handlers will be checked. You can change this behavior with the `final` parameter:

```python
@bot.on.message(Text("/start"), final=False)
async def non_final_handler(message: Message) -> None:
    # This handler will be executed, but other matching handlers will also be checked
    ...

@bot.on.message(Text("/start"))
async def another_handler(message: Message) -> None:
    # This handler will also be executed if the first handler is not final
    ...
```

## Middleware

Middleware allows you to process updates before they reach handlers:

```python
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

### Middleware Chain

You can register multiple middleware functions, which will be executed in the order they were registered:

```python
@bot.dispatch.middleware
async def first_middleware(update: Update, next_handler: Callable) -> Any:
    print("First middleware - pre")
    result = await next_handler(update)
    print("First middleware - post")
    return result

@bot.dispatch.middleware
async def second_middleware(update: Update, next_handler: Callable) -> Any:
    print("Second middleware - pre")
    result = await next_handler(update)
    print("Second middleware - post")
    return result
```

The execution order will be:
1. First middleware - pre
2. Second middleware - pre
3. Handler
4. Second middleware - post
5. First middleware - post

## Error Handling

You can add error handling to the dispatcher:

```python
from mubble.tools.error_handler import ErrorHandler

error_handler = ErrorHandler()

@error_handler.register
async def handle_error(error: Exception, event: Any) -> None:
    logger.error(f"Error processing event: {error}")

bot.dispatch.error_handler = error_handler
```

## Advanced Usage

### Custom Dispatch Implementation

You can create your own dispatcher by implementing the `ABCDispatch` interface:

```python
from mubble.bot import ABCDispatch

class MyCustomDispatch(ABCDispatch):
    # Implement the required methods
    ...
```

### Context Injection

The dispatcher automatically injects the context object into handlers that request it:

```python
@bot.on.message(Text("/start"))
async def start_handler(message: Message, ctx: Context) -> None:
    # The context is automatically injected
    ctx.set("user_id", message.from_user.id)
```

### API Client Injection

The dispatcher can also inject the API client:

```python
@bot.on.message(Text("/start"))
async def start_handler(message: Message, api: API) -> None:
    # The API client is automatically injected
    me = (await api.get_me()).unwrap()
    await message.answer(f"Hello! I'm {me.first_name}")
```

## Next Steps

Now that you understand dispatching, you can explore:

- [Handlers](handlers.md)
- [Rules](rules.md)
- [Middleware](middleware.md)
- [Error Handling](error-handling.md) 