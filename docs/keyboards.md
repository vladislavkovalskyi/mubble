# Keyboards

This document explains how to use reply keyboards in Mubble for Telegram bots.

## Overview

Telegram offers several types of keyboards to enhance user interaction:

1. **Reply Keyboards**: Custom keyboards that appear below the message input field
2. **Inline Keyboards**: Buttons attached to specific messages (covered in [Inline Keyboards](inline-keyboards.md))
3. **Keyboard Removal**: Removing custom keyboards to show the default keyboard

Mubble provides convenient classes and methods to work with all these keyboard types.

## Reply Keyboards

Reply keyboards replace the default keyboard with custom buttons. When a user taps a button, the button's text is sent as a message.

### Basic Reply Keyboard

```python
from mubble import Message, ReplyKeyboardMarkup, KeyboardButton

@bot.on.message()
async def handler(message: Message) -> None:
    # Create a simple keyboard with text buttons
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Button 1"),
                KeyboardButton(text="Button 2")
            ],
            [
                KeyboardButton(text="Button 3")
            ]
        ],
        resize_keyboard=True  # Make the keyboard smaller
    )
    
    # Send a message with the keyboard
    await message.answer(
        "Please choose an option:",
        reply_markup=keyboard
    )
```

### Keyboard Options

You can customize the keyboard appearance and behavior:

```python
from mubble import Message, ReplyKeyboardMarkup, KeyboardButton

@bot.on.message()
async def handler(message: Message) -> None:
    # Create a keyboard with various options
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Button 1"),
                KeyboardButton(text="Button 2")
            ],
            [
                KeyboardButton(text="Button 3")
            ]
        ],
        resize_keyboard=True,  # Make the keyboard smaller
        one_time_keyboard=True,  # Hide keyboard after use
        input_field_placeholder="Select an option",  # Placeholder text in the input field
        selective=True  # Show keyboard only to specific users in a group
    )
    
    # Send a message with the keyboard
    await message.answer(
        "Please choose an option:",
        reply_markup=keyboard
    )
```

### Special Button Types

Telegram supports special button types that can request user data:

```python
from mubble import Message, ReplyKeyboardMarkup, KeyboardButton

@bot.on.message()
async def handler(message: Message) -> None:
    # Create a keyboard with special buttons
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="Share Contact",
                    request_contact=True  # Request user's phone number
                ),
                KeyboardButton(
                    text="Share Location",
                    request_location=True  # Request user's location
                )
            ],
            [
                KeyboardButton(
                    text="Create Poll",
                    request_poll=KeyboardButtonPollType(type="regular")  # Request to create a poll
                )
            ],
            [
                KeyboardButton(
                    text="Request Chat",
                    request_chat=KeyboardButtonRequestChat(
                        request_id=1,
                        chat_is_channel=True
                    )  # Request a chat
                )
            ],
            [
                KeyboardButton(
                    text="Request User",
                    request_user=KeyboardButtonRequestUser(
                        request_id=1
                    )  # Request a user
                )
            ]
        ],
        resize_keyboard=True
    )
    
    # Send a message with the keyboard
    await message.answer(
        "Please choose an option:",
        reply_markup=keyboard
    )
```

### Handling Button Presses

When a user presses a button, the button's text is sent as a regular message:

```python
from mubble import Message
from mubble.rules import Text

@bot.on.message(Text("Button 1"))
async def button1_handler(message: Message) -> None:
    await message.answer("You pressed Button 1!")

@bot.on.message(Text("Button 2"))
async def button2_handler(message: Message) -> None:
    await message.answer("You pressed Button 2!")

@bot.on.message(Text("Button 3"))
async def button3_handler(message: Message) -> None:
    await message.answer("You pressed Button 3!")
```

## Keyboard Removal

You can remove a custom keyboard and return to the default keyboard:

```python
from mubble import Message, ReplyKeyboardRemove

@bot.on.message(Text("Remove Keyboard"))
async def remove_keyboard_handler(message: Message) -> None:
    # Create a keyboard removal object
    keyboard_removal = ReplyKeyboardRemove(
        remove_keyboard=True,
        selective=False  # Remove for all users in a group
    )
    
    # Send a message with the keyboard removal
    await message.answer(
        "Keyboard removed.",
        reply_markup=keyboard_removal
    )
```

## Advanced Keyboard Patterns

### Dynamic Keyboards

You can create keyboards dynamically based on data:

```python
from mubble import Message, ReplyKeyboardMarkup, KeyboardButton
from mubble.rules import Text

# Sample data
items = ["Apple", "Banana", "Cherry", "Date", "Elderberry"]

@bot.on.message(Text("/items"))
async def items_handler(message: Message) -> None:
    # Create a keyboard with items (2 items per row)
    keyboard_buttons = []
    row = []
    
    for i, item in enumerate(items):
        row.append(KeyboardButton(text=item))
        
        # Add 2 buttons per row
        if len(row) == 2 or i == len(items) - 1:
            keyboard_buttons.append(row)
            row = []
    
    # Create the keyboard
    keyboard = ReplyKeyboardMarkup(
        keyboard=keyboard_buttons,
        resize_keyboard=True
    )
    
    # Send a message with the keyboard
    await message.answer(
        "Please choose an item:",
        reply_markup=keyboard
    )
```

### Persistent Keyboard

You can create a persistent keyboard that stays across messages:

```python
from mubble import Message, ReplyKeyboardMarkup, KeyboardButton
from mubble.rules import Text

# Create a persistent keyboard
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Help"),
            KeyboardButton(text="Settings")
        ],
        [
            KeyboardButton(text="About")
        ]
    ],
    resize_keyboard=True
)

@bot.on.message(Text("/start"))
async def start_handler(message: Message) -> None:
    # Send a welcome message with the keyboard
    await message.answer(
        "Welcome to the bot! Use the keyboard below to navigate.",
        reply_markup=main_keyboard
    )

# Always send the same keyboard with every response
@bot.on.message(Text("Help"))
async def help_handler(message: Message) -> None:
    await message.answer(
        "This is the help message.",
        reply_markup=main_keyboard
    )

@bot.on.message(Text("Settings"))
async def settings_handler(message: Message) -> None:
    await message.answer(
        "Here are your settings.",
        reply_markup=main_keyboard
    )

@bot.on.message(Text("About"))
async def about_handler(message: Message) -> None:
    await message.answer(
        "This bot was created with Mubble.",
        reply_markup=main_keyboard
    )
```

### Menu Navigation

You can create a menu system with multiple levels:

```python
from mubble import Message, ReplyKeyboardMarkup, KeyboardButton
from mubble.rules import Text

# Create keyboards for different menus
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Products"),
            KeyboardButton(text="Services")
        ],
        [
            KeyboardButton(text="Contact"),
            KeyboardButton(text="About")
        ]
    ],
    resize_keyboard=True
)

products_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Product A"),
            KeyboardButton(text="Product B")
        ],
        [
            KeyboardButton(text="Product C")
        ],
        [
            KeyboardButton(text="Back to Main Menu")
        ]
    ],
    resize_keyboard=True
)

services_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Service X"),
            KeyboardButton(text="Service Y")
        ],
        [
            KeyboardButton(text="Service Z")
        ],
        [
            KeyboardButton(text="Back to Main Menu")
        ]
    ],
    resize_keyboard=True
)

@bot.on.message(Text("/start"))
async def start_handler(message: Message) -> None:
    await message.answer(
        "Welcome to the bot! Use the keyboard to navigate.",
        reply_markup=main_menu
    )

@bot.on.message(Text("Products"))
async def products_handler(message: Message) -> None:
    await message.answer(
        "Here are our products:",
        reply_markup=products_menu
    )

@bot.on.message(Text("Services"))
async def services_handler(message: Message) -> None:
    await message.answer(
        "Here are our services:",
        reply_markup=services_menu
    )

@bot.on.message(Text("Back to Main Menu"))
async def back_to_main_handler(message: Message) -> None:
    await message.answer(
        "Main menu:",
        reply_markup=main_menu
    )

# Handle individual product/service selections
@bot.on.message(Text("Product A"))
async def product_a_handler(message: Message) -> None:
    await message.answer(
        "Product A details...",
        reply_markup=products_menu
    )

# Add handlers for other products and services...
```

### Keyboard with User State

You can show different keyboards based on user state:

```python
from mubble import Message, ReplyKeyboardMarkup, KeyboardButton, Context
from mubble.rules import Text

# User states
user_states = {}

# Keyboards for different states
guest_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Login"),
            KeyboardButton(text="Register")
        ],
        [
            KeyboardButton(text="About")
        ]
    ],
    resize_keyboard=True
)

user_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Profile"),
            KeyboardButton(text="Settings")
        ],
        [
            KeyboardButton(text="Logout")
        ]
    ],
    resize_keyboard=True
)

@bot.on.message(Text("/start"))
async def start_handler(message: Message) -> None:
    # Check if user is logged in
    user_id = message.from_user.id
    is_logged_in = user_states.get(user_id, False)
    
    if is_logged_in:
        await message.answer(
            "Welcome back!",
            reply_markup=user_keyboard
        )
    else:
        await message.answer(
            "Welcome! Please login or register.",
            reply_markup=guest_keyboard
        )

@bot.on.message(Text("Login"))
async def login_handler(message: Message) -> None:
    # Simulate login
    user_id = message.from_user.id
    user_states[user_id] = True
    
    await message.answer(
        "You are now logged in!",
        reply_markup=user_keyboard
    )

@bot.on.message(Text("Logout"))
async def logout_handler(message: Message) -> None:
    # Simulate logout
    user_id = message.from_user.id
    user_states[user_id] = False
    
    await message.answer(
        "You have been logged out.",
        reply_markup=guest_keyboard
    )
```

## Keyboard Builders

Mubble provides builder classes to create keyboards more easily:

```python
from mubble import Message, ReplyKeyboardBuilder, KeyboardButton
from mubble.rules import Text

@bot.on.message(Text("/keyboard"))
async def keyboard_handler(message: Message) -> None:
    # Create a keyboard builder
    builder = ReplyKeyboardBuilder()
    
    # Add buttons
    builder.add(KeyboardButton(text="Button 1"))
    builder.add(KeyboardButton(text="Button 2"))
    builder.add(KeyboardButton(text="Button 3"))
    builder.add(KeyboardButton(text="Button 4"))
    
    # Adjust the layout (2 buttons per row)
    builder.adjust(2)
    
    # Build the keyboard
    keyboard = builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    # Send a message with the keyboard
    await message.answer(
        "Here's a keyboard:",
        reply_markup=keyboard
    )
```

## Best Practices

### Keep Keyboards Simple

Don't overwhelm users with too many buttons. Keep keyboards simple and intuitive.

### Provide Clear Instructions

Always provide clear instructions on how to use the keyboard.

### Use Appropriate Button Text

Button text should be concise and descriptive.

### Consider Screen Size

Remember that users may have different screen sizes. Use `resize_keyboard=True` to make the keyboard more compact.

### Provide Keyboard Removal Option

Always provide a way for users to remove the keyboard if they want to.

### Test on Different Devices

Test your keyboards on different devices to ensure they look good and work properly.

## Next Steps

Now that you understand reply keyboards in Mubble, you can explore:

- [Inline Keyboards](inline-keyboards.md)
- [Callback Queries](callback-queries.md)
- [State Management](state-management.md)
- [Handlers](handlers.md) 