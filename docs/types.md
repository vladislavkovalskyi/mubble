# Types

This document explains the type system in Mubble and the various types available for working with the Telegram Bot API.

## Overview

Mubble provides a comprehensive set of type-hinted classes that represent Telegram Bot API objects. These types are designed to be:

- **Type-safe**: All types have proper type annotations for better IDE support and code safety
- **Immutable**: Most types are immutable to prevent accidental modifications
- **Convenient**: Types include helper methods for common operations
- **Complete**: All Telegram Bot API objects are represented

## Core Types

### Update

The `Update` type represents an incoming update from Telegram:

```python
from mubble import Update

async def handle_update(update: Update) -> None:
    if update.message:
        # Handle message
        ...
    elif update.callback_query:
        # Handle callback query
        ...
    # etc.
```

### Message

The `Message` type represents a message:

```python
from mubble import Message

async def handle_message(message: Message) -> None:
    # Access message properties
    text = message.text
    chat_id = message.chat.id
    user = message.from_user
    
    # Reply to the message
    await message.reply("Hello!")
```

### CallbackQuery

The `CallbackQuery` type represents a callback query from an inline keyboard:

```python
from mubble import CallbackQuery

async def handle_callback_query(callback_query: CallbackQuery) -> None:
    # Access callback query properties
    data = callback_query.data
    message = callback_query.message
    
    # Answer the callback query
    await callback_query.answer("You clicked a button!")
    
    # Edit the message
    await callback_query.message.edit_text("Button clicked!")
```

### InlineQuery

The `InlineQuery` type represents an inline query:

```python
from mubble import InlineQuery
from mubble.types import InlineQueryResultArticle, InputTextMessageContent

async def handle_inline_query(inline_query: InlineQuery) -> None:
    # Access inline query properties
    query = inline_query.query
    
    # Answer the inline query
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

### ChatJoinRequest

The `ChatJoinRequest` type represents a request to join a chat:

```python
from mubble import ChatJoinRequest

async def handle_join_request(join_request: ChatJoinRequest) -> None:
    # Access join request properties
    user = join_request.from_user
    chat = join_request.chat
    
    # Approve the request
    await join_request.approve()
    
    # Or decline the request
    # await join_request.decline()
```

## User Types

### User

The `User` type represents a Telegram user:

```python
from mubble import User

def process_user(user: User) -> None:
    # Access user properties
    user_id = user.id
    username = user.username
    full_name = user.full_name  # Convenience property
```

### Chat

The `Chat` type represents a Telegram chat:

```python
from mubble import Chat
from mubble.types.enums import ChatType

def process_chat(chat: Chat) -> None:
    # Access chat properties
    chat_id = chat.id
    chat_type = chat.type
    
    # Check chat type
    if chat.type == ChatType.PRIVATE:
        # Private chat
        ...
    elif chat.type == ChatType.GROUP:
        # Group chat
        ...
```

## Media Types

### PhotoSize

The `PhotoSize` type represents a photo:

```python
from mubble import PhotoSize

async def process_photo(photo: list[PhotoSize]) -> None:
    # Get the largest photo
    largest_photo = photo[-1]
    
    # Access photo properties
    file_id = largest_photo.file_id
    width = largest_photo.width
    height = largest_photo.height
```

### Audio, Document, Video, etc.

Mubble provides types for all media types:

```python
from mubble import Audio, Document, Video, Voice, VideoNote, Animation

async def process_media(message: Message) -> None:
    if message.audio:
        # Handle audio
        audio = message.audio
        duration = audio.duration
        
    elif message.document:
        # Handle document
        document = message.document
        file_name = document.file_name
        
    elif message.video:
        # Handle video
        video = message.video
        width = video.width
        height = video.height
```

## Keyboard Types

### InlineKeyboardMarkup

The `InlineKeyboardMarkup` type represents an inline keyboard:

```python
from mubble.types import InlineKeyboardMarkup, InlineKeyboardButton

# Create an inline keyboard
keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Button 1", callback_data="btn1"),
            InlineKeyboardButton(text="Button 2", callback_data="btn2")
        ],
        [
            InlineKeyboardButton(text="URL", url="https://example.com")
        ]
    ]
)

# Send a message with the keyboard
await api.send_message(
    chat_id=123456789,
    text="Choose an option:",
    reply_markup=keyboard
)
```

### ReplyKeyboardMarkup

The `ReplyKeyboardMarkup` type represents a reply keyboard:

```python
from mubble.types import ReplyKeyboardMarkup, KeyboardButton

# Create a reply keyboard
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
    resize_keyboard=True
)

# Send a message with the keyboard
await api.send_message(
    chat_id=123456789,
    text="Choose an option:",
    reply_markup=keyboard
)
```

## Input Types

### InputFile

The `InputFile` type represents a file to be uploaded:

```python
from mubble.types import InputFile

# Create an input file from a local file
input_file = InputFile("path/to/file.jpg")

# Create an input file from bytes
with open("path/to/file.jpg", "rb") as f:
    file_bytes = f.read()
    input_file = InputFile(file_bytes, filename="photo.jpg")

# Send a photo
await api.send_photo(
    chat_id=123456789,
    photo=input_file,
    caption="Beautiful photo"
)
```

## Enums

Mubble provides enums for various Telegram constants:

```python
from mubble.types.enums import ChatType, ParseMode, MessageEntityType

# Check chat type
if chat.type == ChatType.PRIVATE:
    # Private chat
    ...

# Specify parse mode
await api.send_message(
    chat_id=123456789,
    text="*Bold* _italic_",
    parse_mode=ParseMode.MARKDOWN
)

# Check entity type
for entity in message.entities:
    if entity.type == MessageEntityType.URL:
        # URL entity
        ...
```

## Custom Types

### Model

The `Model` class is the base class for all Mubble types. You can create your own types by inheriting from it:

```python
from mubble import Model

class MyCustomType(Model):
    def __init__(self, name: str, value: int) -> None:
        self.name = name
        self.value = value
```

## Next Steps

Now that you understand the type system, you can explore:

- [API Client](api-client.md)
- [Handlers](handlers.md)
- [Rules](rules.md)
- [Callback Queries](callback-queries.md) 