# Inline Keyboards

This document explains how to create and use inline keyboards in Mubble.

## Overview

Inline keyboards are a powerful way to add interactive buttons to your bot's messages. Unlike reply keyboards, inline keyboards:

- Are attached to specific messages
- Don't disappear after being pressed
- Can be updated dynamically
- Generate callback queries when pressed

## Creating Inline Keyboards

Mubble provides a convenient builder API for creating inline keyboards:

```python
from mubble.tools.keyboard import InlineKeyboard, InlineButton

# Create a simple inline keyboard
keyboard = (
    InlineKeyboard()
    .add(InlineButton("Button 1", callback_data="btn1"))
    .add(InlineButton("Button 2", callback_data="btn2"))
).get_markup()
```

### Adding Buttons

You can add buttons in various ways:

```python
# Add buttons in a single row
keyboard = (
    InlineKeyboard()
    .add(InlineButton("Button 1", callback_data="btn1"))
    .add(InlineButton("Button 2", callback_data="btn2"))
).get_markup()

# Add buttons in multiple rows
keyboard = (
    InlineKeyboard()
    .add(InlineButton("Row 1, Button 1", callback_data="r1b1"))
    .row()  # Start a new row
    .add(InlineButton("Row 2, Button 1", callback_data="r2b1"))
    .add(InlineButton("Row 2, Button 2", callback_data="r2b2"))
).get_markup()

# Add multiple buttons at once
keyboard = (
    InlineKeyboard()
    .add(
        InlineButton("Button 1", callback_data="btn1"),
        InlineButton("Button 2", callback_data="btn2")
    )
    .row()
    .add(InlineButton("Button 3", callback_data="btn3"))
).get_markup()
```

### Button Types

Inline buttons can have different actions:

```python
# Callback data button (sends a callback query)
callback_button = InlineButton("Callback", callback_data="callback_data")

# URL button (opens a URL)
url_button = InlineButton("Open URL", url="https://example.com")

# Switch inline query button (starts an inline query in the current chat)
switch_button = InlineButton("Search", switch_inline_query="query")

# Switch inline query current chat button (starts an inline query in a different chat)
switch_current_button = InlineButton(
    "Search in this chat",
    switch_inline_query_current_chat="query"
)

# Login URL button (for Telegram Login)
login_button = InlineButton(
    "Login",
    login_url=LoginUrl(
        url="https://example.com/login",
        forward_text="Login to Example",
        bot_username="ExampleBot"
    )
)

# Callback game button (for games)
game_button = InlineButton("Play Game", callback_game=CallbackGame())

# Pay button (for payments)
pay_button = InlineButton("Pay", pay=True)
```

## Using Inline Keyboards

### Sending Messages with Keyboards

You can send a message with an inline keyboard:

```python
from mubble import Message
from mubble.rules import Text

@bot.on.message(Text("/menu"))
async def menu_handler(message: Message) -> None:
    keyboard = (
        InlineKeyboard()
        .add(InlineButton("Option 1", callback_data="option_1"))
        .add(InlineButton("Option 2", callback_data="option_2"))
    ).get_markup()
    
    await message.answer("Please select an option:", reply_markup=keyboard)
```

### Updating Keyboards

You can update the keyboard of an existing message:

```python
from mubble import CallbackQuery

@bot.on.callback_query(lambda cq: cq.data == "option_1")
async def option_1_handler(callback_query: CallbackQuery) -> None:
    # Create a new keyboard
    new_keyboard = (
        InlineKeyboard()
        .add(InlineButton("Back", callback_data="back"))
    ).get_markup()
    
    # Update the message with a new text and keyboard
    await callback_query.message.edit_text(
        "You selected Option 1",
        reply_markup=new_keyboard
    )
    
    # Or just update the keyboard
    # await callback_query.message.edit_reply_markup(reply_markup=new_keyboard)
```

## Advanced Keyboard Patterns

### Grid Layout

You can create a grid of buttons:

```python
def create_grid_keyboard(rows: int, cols: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboard()
    
    for r in range(rows):
        for c in range(cols):
            button_text = f"Button {r*cols + c + 1}"
            callback_data = f"btn_{r}_{c}"
            keyboard.add(InlineButton(button_text, callback_data=callback_data))
        
        if r < rows - 1:  # Don't add a row after the last row
            keyboard.row()
    
    return keyboard.get_markup()

# Create a 3x3 grid
grid_keyboard = create_grid_keyboard(3, 3)
```

### Pagination

You can create a paginated keyboard:

```python
def create_pagination_keyboard(
    items: list[str],
    page: int,
    items_per_page: int = 5
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboard()
    
    # Calculate total pages
    total_pages = (len(items) + items_per_page - 1) // items_per_page
    
    # Get items for the current page
    start_idx = (page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, len(items))
    page_items = items[start_idx:end_idx]
    
    # Add item buttons
    for i, item in enumerate(page_items):
        item_idx = start_idx + i
        keyboard.add(InlineButton(item, callback_data=f"item_{item_idx}"))
        keyboard.row()
    
    # Add navigation buttons
    nav_buttons = []
    
    if page > 1:
        nav_buttons.append(InlineButton("◀️ Prev", callback_data=f"page_{page-1}"))
    
    nav_buttons.append(InlineButton(f"{page}/{total_pages}", callback_data="current_page"))
    
    if page < total_pages:
        nav_buttons.append(InlineButton("Next ▶️", callback_data=f"page_{page+1}"))
    
    keyboard.add(*nav_buttons)
    
    return keyboard.get_markup()

# Create a paginated keyboard
items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5", "Item 6", "Item 7"]
pagination_keyboard = create_pagination_keyboard(items, page=1, items_per_page=3)
```

### Dynamic Keyboards

You can create keyboards dynamically based on data:

```python
def create_product_keyboard(products: list[dict]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboard()
    
    for product in products:
        product_id = product["id"]
        product_name = product["name"]
        product_price = product["price"]
        
        button_text = f"{product_name} - ${product_price}"
        callback_data = f"product_{product_id}"
        
        keyboard.add(InlineButton(button_text, callback_data=callback_data))
        keyboard.row()
    
    # Add a back button
    keyboard.add(InlineButton("Back to Menu", callback_data="back_to_menu"))
    
    return keyboard.get_markup()

# Create a keyboard with products
products = [
    {"id": 1, "name": "Product A", "price": 9.99},
    {"id": 2, "name": "Product B", "price": 19.99},
    {"id": 3, "name": "Product C", "price": 29.99}
]
product_keyboard = create_product_keyboard(products)
```

## Serializing Complex Data

For complex callback data, you can use serialization:

```python
import dataclasses
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
```

## Best Practices

### Keep Keyboards Simple

- Use clear, concise button labels
- Limit the number of buttons to avoid overwhelming users
- Group related buttons together
- Use icons sparingly to enhance readability

### Provide Feedback

- Always answer callback queries to provide feedback
- Update the message text or keyboard to reflect the new state
- Consider using `answer()` with `show_alert=True` for important messages

### Handle Edge Cases

- Consider what happens if a user clicks a button multiple times
- Handle cases where the message is too old to edit
- Provide a way for users to go back or cancel operations

## Next Steps

Now that you understand inline keyboards, you can explore:

- [Callback Queries](callback-queries.md)
- [State Management](state-management.md)
- [Handlers](handlers.md)
- [Rules](rules.md) 