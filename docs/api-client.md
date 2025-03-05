# API Client

The API client is a core component of Mubble that handles communication with the Telegram Bot API. This document explains how to use and customize the API client.

## Overview

Mubble's API client is designed to be:

- **Fast**: Optimized for high-performance API calls
- **Type-safe**: All methods and responses are fully type-hinted
- **Flexible**: Supports different HTTP client implementations
- **Error-aware**: Provides clear error handling mechanisms

## Basic Usage

### Creating an API Client

To create an API client, you need a bot token:

```python
from mubble import API, Token

# Create an API instance with a token string
api = API(token=Token("123456789:ABCDefGhIJKlmnOPQRstUVwxyz"))

# Or load the token from an environment variable
api = API(token=Token.from_env())  # Uses the TOKEN environment variable
```

### Making API Calls

All Telegram Bot API methods are available as methods on the API instance:

```python
# Get information about the bot
me = await api.get_me()

# Send a message
message = await api.send_message(
    chat_id=123456789,
    text="Hello, world!"
)
```

### Handling Responses

API methods return an `APIResponse` object that wraps the result or error:

```python
response = await api.send_message(chat_id=123456789, text="Hello!")

# Check if the request was successful
if response.is_ok:
    # Access the result
    message = response.unwrap()
    print(f"Message sent with ID: {message.message_id}")
else:
    # Handle the error
    error = response.unwrap_err()
    print(f"Error: {error.description}")
```

You can also use the `unwrap()` method which returns the result or raises an exception:

```python
try:
    message = (await api.send_message(chat_id=123456789, text="Hello!")).unwrap()
    print(f"Message sent with ID: {message.message_id}")
except APIError as e:
    print(f"Error: {e.description}")
```

## HTTP Clients

Mubble supports different HTTP client implementations:

### AiohttpClient (Default)

The default client uses `aiohttp`:

```python
from mubble import API, Token
from mubble.client import AiohttpClient

api = API(
    token=Token("YOUR_BOT_TOKEN"),
    client=AiohttpClient()
)
```

### AiosonicClient

An alternative client based on `aiosonic` for potentially better performance:

```python
from mubble import API, Token
from mubble.client import AiosonicClient

api = API(
    token=Token("YOUR_BOT_TOKEN"),
    client=AiosonicClient()
)
```

### Custom Clients

You can create your own client by implementing the `ABCClient` interface:

```python
from mubble.client import ABCClient

class MyCustomClient(ABCClient):
    async def request(self, method: str, url: str, **kwargs) -> dict:
        # Implement your custom request logic
        ...
```

## Advanced Usage

### Setting API Parameters

You can customize various API parameters:

```python
from mubble import API, Token

api = API(
    token=Token("YOUR_BOT_TOKEN"),
    base_url="https://api.telegram.org",  # Custom API URL
    api_version="v1",  # API version
    timeout=30.0,  # Request timeout in seconds
)
```

### File Uploads

Mubble supports file uploads in various formats:

```python
from mubble import API, Token
from mubble.types import InputFile

api = API(token=Token("YOUR_BOT_TOKEN"))

# Upload a file from disk
await api.send_document(
    chat_id=123456789,
    document=InputFile("path/to/document.pdf")
)

# Upload a file from bytes
with open("path/to/photo.jpg", "rb") as f:
    file_bytes = f.read()
    
await api.send_photo(
    chat_id=123456789,
    photo=InputFile(file_bytes, filename="photo.jpg")
)
```

### Error Handling

Mubble provides detailed error information:

```python
from mubble import API, Token, APIError, APIServerError

api = API(token=Token("YOUR_BOT_TOKEN"))

try:
    result = (await api.send_message(chat_id=123456789, text="Hello!")).unwrap()
except APIError as e:
    # Client-side error (e.g., invalid parameters)
    print(f"API Error: {e.description}")
    print(f"Error Code: {e.error_code}")
except APIServerError as e:
    # Server-side error
    print(f"Server Error: {e}")
```

## API Methods

All methods from the [Telegram Bot API](https://core.telegram.org/bots/api) are available. Here are some commonly used methods:

### Messages

```python
# Send a text message
await api.send_message(chat_id=123456789, text="Hello!")

# Send a message with formatting
await api.send_message(
    chat_id=123456789,
    text="*Bold* _italic_ `code`",
    parse_mode="MarkdownV2"
)

# Send a message with a reply markup
from mubble.tools.keyboard import InlineKeyboard, InlineButton

keyboard = (
    InlineKeyboard()
    .add(InlineButton("Button 1", callback_data="btn1"))
    .add(InlineButton("Button 2", callback_data="btn2"))
).get_markup()

await api.send_message(
    chat_id=123456789,
    text="Choose an option:",
    reply_markup=keyboard
)
```

### Media

```python
# Send a photo
await api.send_photo(
    chat_id=123456789,
    photo=InputFile("path/to/photo.jpg"),
    caption="Beautiful photo"
)

# Send a document
await api.send_document(
    chat_id=123456789,
    document=InputFile("path/to/document.pdf"),
    caption="Important document"
)
```

### Chat Actions

```python
# Show "typing..." status
await api.send_chat_action(
    chat_id=123456789,
    action="typing"
)
```

## Next Steps

Now that you understand how to use the API client, you can explore:

- [Bot Structure](bot-structure.md)
- [Types](types.md)
- [Handlers](handlers.md) 