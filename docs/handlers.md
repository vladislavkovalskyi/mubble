# Handlers

Handlers in Mubble are functions that process specific types of updates. This document explains how to create and use handlers.

## Overview

Handlers are the core of your bot's functionality. They are registered with the dispatcher and executed when their associated rules match an incoming update.

## Basic Handlers

### Message Handlers

Message handlers process incoming messages:

```python
from mubble import Message
from mubble.rules import Text

@bot.on.message(Text("/start"))
async def start_handler(message: Message) -> None:
    await message.answer(f"Hello, {message.from_user.full_name}!")
```

### Callback Query Handlers

Callback query handlers process button presses in inline keyboards:

```python
from mubble import CallbackQuery

@bot.on.callback_query(lambda cq: cq.data == "option_1")
async def option_1_handler(callback_query: CallbackQuery) -> None:
    await callback_query.answer("You selected Option 1!")
    await callback_query.message.edit_text("Option 1 selected")
```

### Inline Query Handlers

Inline query handlers process inline queries:

```python
from mubble import InlineQuery
from mubble.types import InlineQueryResultArticle, InputTextMessageContent

@bot.on.inline_query()
async def inline_handler(inline_query: InlineQuery) -> None:
    await inline_query.answer(
        results=[
            InlineQueryResultArticle(
                id="1",
                title="Example",
                input_message_content=InputTextMessageContent(
                    message_text="This is an example"
                )
            )
        ]
    )
```

### Chat Join Request Handlers

Chat join request handlers process requests to join chats:

```python
from mubble import ChatJoinRequest

@bot.on.chat_join_request()
async def join_request_handler(join_request: ChatJoinRequest) -> None:
    await join_request.approve()
    await bot.api.send_message(
        chat_id=join_request.user_chat_id,
        text=f"Welcome to {join_request.chat.title}!"
    )
```

## Handler Parameters

Handlers can receive various parameters:

### Event Object

The first parameter is always the event object (Message, CallbackQuery, etc.):

```python
@bot.on.message(Text("/start"))
async def start_handler(message: Message) -> None:
    # 'message' is the event object
    await message.answer("Hello!")
```

### Context

You can receive the context object:

```python
from mubble import Message, Context

@bot.on.message(Text("/start"))
async def start_handler(message: Message, ctx: Context) -> None:
    # Store data in context
    ctx.set("user_id", message.from_user.id)
    await message.answer("Hello!")
```

### Rule Parameters

Rules can extract parameters from updates:

```python
from mubble.rules import Markup

@bot.on.message(Markup(["/random <a:int> <b:int>"]))
async def random_handler(message: Message, a: int, b: int) -> None:
    # 'a' and 'b' are extracted from the message text
    import random
    await message.answer(f"Random number: {random.randint(a, b)}")
```

### API Client

You can receive the API client:

```python
from mubble import API, Message

@bot.on.message(Text("/start"))
async def start_handler(message: Message, api: API) -> None:
    # Use the API client directly
    me = (await api.get_me()).unwrap()
    await message.answer(f"Hello! I'm {me.first_name}")
```

## Handler Registration

### Decorator Syntax

The most common way to register handlers is using decorators:

```python
@bot.on.message(Text("/start"))
async def start_handler(message: Message) -> None:
    await message.answer("Hello!")
```

### Manual Registration

You can also register handlers manually:

```python
async def start_handler(message: Message) -> None:
    await message.answer("Hello!")

bot.on.message(Text("/start"))(start_handler)
```

### Handler Priority

You can specify the priority of a handler:

```python
@bot.on.message(Text("/start"), priority=10)
async def high_priority_handler(message: Message) -> None:
    # This handler will be checked before lower priority handlers
    await message.answer("High priority handler")

@bot.on.message(Text("/start"), priority=1)
async def low_priority_handler(message: Message) -> None:
    # This handler will only be executed if higher priority handlers don't match
    await message.answer("Low priority handler")
```

## Handler Responses

Handlers can respond to updates in various ways:

### Direct Responses

You can respond directly using methods on the event object:

```python
@bot.on.message(Text("/start"))
async def start_handler(message: Message) -> None:
    # Send a text response
    await message.answer("Hello!")
    
    # Reply to the message
    await message.reply("This is a reply")
    
    # Edit the message (if it's your message)
    await message.edit_text("Edited message")
```

### Using the API Client

You can use the API client for more complex responses:

```python
@bot.on.message(Text("/photo"))
async def photo_handler(message: Message, api: API) -> None:
    # Send a photo
    await api.send_photo(
        chat_id=message.chat.id,
        photo=InputFile("path/to/photo.jpg"),
        caption="Beautiful photo"
    )
```

## Handler Flow Control

### Final Handlers

By default, if a handler is executed, no other handlers will be checked. You can change this behavior with the `final` parameter:

```python
@bot.on.message(Text("/start"), final=False)
async def non_final_handler(message: Message) -> None:
    # This handler will be executed, but other matching handlers will also be checked
    await message.answer("First handler")

@bot.on.message(Text("/start"))
async def another_handler(message: Message) -> None:
    # This handler will also be executed if the first handler is not final
    await message.answer("Second handler")
```

### Stopping Propagation

You can stop the propagation of an update to other handlers:

```python
@bot.on.message(Text("/start"), final=False)
async def handler(message: Message, ctx: Context) -> None:
    await message.answer("First handler")
    
    # Stop propagation to other handlers
    ctx.stop_propagation()
```

## Error Handling

You can handle errors that occur in handlers:

```python
from mubble.tools.error_handler import ErrorHandler

error_handler = ErrorHandler()

@error_handler.register
async def handle_error(error: Exception, event: Any) -> None:
    logger.error(f"Error processing event: {error}")
    
    # Notify the user
    if hasattr(event, "answer"):
        await event.answer("An error occurred while processing your request")

bot.dispatch.error_handler = error_handler
```

## Next Steps

Now that you understand handlers, you can explore:

- [Rules](rules.md)
- [Dispatching](dispatching.md)
- [Context](global-context.md)
- [Callback Queries](callback-queries.md)