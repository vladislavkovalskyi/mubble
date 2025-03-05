# Callback Queries

This document explains how to work with callback queries in Mubble, which are generated when users interact with inline keyboards.

## Overview

Callback queries are generated when a user clicks a button in an inline keyboard. They allow your bot to respond to user interactions with messages.

## Basic Usage

### Creating Inline Keyboards

To receive callback queries, you first need to send a message with an inline keyboard:

```python
from mubble import API, Message, Token
from mubble.tools.keyboard import InlineKeyboard, InlineButton
from mubble.rules import Text

api = API(token=Token("YOUR_BOT_TOKEN"))
bot = Mubble(api)

@bot.on.message(Text("/menu"))
async def menu_handler(message: Message) -> None:
    # Create an inline keyboard
    keyboard = (
        InlineKeyboard()
        .add(InlineButton("Option 1", callback_data="option_1"))
        .add(InlineButton("Option 2", callback_data="option_2"))
    ).get_markup()
    
    # Send a message with the keyboard
    await message.answer("Please select an option:", reply_markup=keyboard)
```

### Handling Callback Queries

When a user clicks a button, your bot will receive a callback query that you can handle:

```python
from mubble import CallbackQuery

@bot.on.callback_query(lambda cq: cq.data == "option_1")
async def option_1_handler(callback_query: CallbackQuery) -> None:
    # Answer the callback query (shows a notification to the user)
    await callback_query.answer("You selected Option 1!")
    
    # Edit the message text
    await callback_query.message.edit_text("Option 1 selected")
```

## Callback Query Methods

The `CallbackQuery` object provides several methods for responding to the user:

### answer()

The `answer()` method sends a response to the callback query, which can show a notification to the user:

```python
await callback_query.answer("You clicked a button!")

# Show an alert
await callback_query.answer("This is an alert!", show_alert=True)

# Silent answer (no notification)
await callback_query.answer()
```

### edit_text()

The `edit_text()` method edits the text of the message that contains the inline keyboard:

```python
await callback_query.message.edit_text("New message text")

# Edit text and keep the keyboard
await callback_query.message.edit_text(
    "New message text",
    reply_markup=callback_query.message.reply_markup
)
```

### edit_reply_markup()

The `edit_reply_markup()` method changes the inline keyboard:

```python
from mubble.tools.keyboard import InlineKeyboard, InlineButton

# Create a new keyboard
new_keyboard = (
    InlineKeyboard()
    .add(InlineButton("Back", callback_data="back"))
).get_markup()

# Update the keyboard
await callback_query.message.edit_reply_markup(reply_markup=new_keyboard)
```

## Callback Data Patterns

### Simple String Matching

The simplest way to handle callback queries is to match the callback data string:

```python
@bot.on.callback_query(lambda cq: cq.data == "option_1")
async def option_1_handler(callback_query: CallbackQuery) -> None:
    await callback_query.answer("You selected Option 1!")
```

### Using PayloadEqRule

You can use the `PayloadEqRule` for more readable code:

```python
from mubble.rules import PayloadEqRule

@bot.on.callback_query(PayloadEqRule("option_1"))
async def option_1_handler(callback_query: CallbackQuery) -> None:
    await callback_query.answer("You selected Option 1!")
```

### Parameter Extraction with PayloadMarkupRule

The `PayloadMarkupRule` allows you to extract parameters from callback data:

```python
from mubble.rules import PayloadMarkupRule

# Button with callback_data="product/123"
@bot.on.callback_query(PayloadMarkupRule("product/<product_id:int>"))
async def product_handler(callback_query: CallbackQuery, product_id: int) -> None:
    await callback_query.answer(f"You selected product {product_id}")
```

### Structured Data with PayloadModelRule

For complex data, you can use the `PayloadModelRule` with a serializer:

```python
import dataclasses
from mubble.rules import PayloadModelRule
from mubble.tools.callback_data_serilization import MsgPackSerializer

@dataclasses.dataclass(slots=True, frozen=True)
class Product:
    __key__ = "product"  # Prefix for callback data
    id: int
    name: str
    price: float = dataclasses.field(kw_only=True)

# Create a serializer for the Product class
product_serializer = MsgPackSerializer(Product)

# Create a button with a serialized product
keyboard = (
    InlineKeyboard()
    .add(
        InlineButton(
            "Buy Product",
            callback_data=Product(id=123, name="Example", price=9.99),
            callback_data_serializer=product_serializer
        )
    )
).get_markup()

# Handle the callback query
@bot.on.callback_query(
    PayloadModelRule(Product, serializer=MsgPackSerializer, alias="product")
)
async def product_handler(callback_query: CallbackQuery, product: Product) -> None:
    await callback_query.answer(
        f"You selected {product.name} (${product.price})"
    )
```

## Callback Query Context

You can use the context object to store data between callback queries:

```python
from mubble import Context

@bot.on.callback_query(PayloadEqRule("page/next"))
async def next_page_handler(callback_query: CallbackQuery, ctx: Context) -> None:
    # Get the current page from context (default to 1)
    current_page = ctx.get("page", 1)
    
    # Increment the page
    next_page = current_page + 1
    
    # Store the new page in context
    ctx.set("page", next_page)
    
    # Update the message
    await callback_query.message.edit_text(f"Page {next_page}")
```

## Error Handling

You can handle errors that occur during callback query processing:

```python
from mubble.tools.error_handler import ErrorHandler

error_handler = ErrorHandler()

@error_handler.register
async def handle_error(error: Exception, event: CallbackQuery) -> None:
    logger.error(f"Error processing callback query: {error}")
    
    # Notify the user
    await event.answer("An error occurred while processing your request")

bot.dispatch.error_handler = error_handler
```

## Best Practices

### Keep Callback Data Small

Telegram has a limit on the size of callback data (64 bytes). For complex data, consider:

1. Using IDs and storing the actual data on your server
2. Using a compact serialization format like msgpack
3. Using a URL-safe encoding for binary data

### Update UI Promptly

Always provide immediate feedback to the user:

1. Use `answer()` to acknowledge the button press
2. Update the message text or keyboard to reflect the new state
3. Consider using `answer()` with `show_alert=True` for important messages

### Handle Stale Callbacks

Users might click buttons on old messages. Make sure your handlers can handle this:

```python
@bot.on.callback_query(PayloadEqRule("option_1"))
async def option_1_handler(callback_query: CallbackQuery) -> None:
    try:
        # Try to update the message
        await callback_query.message.edit_text("Option 1 selected")
    except Exception:
        # Message might be too old to edit
        await callback_query.answer("This menu is no longer active")
```

## Next Steps

Now that you understand callback queries, you can explore:

- [Inline Keyboards](inline-keyboards.md)
- [State Management](state-management.md)
- [Handlers](handlers.md)
- [Rules](rules.md) 