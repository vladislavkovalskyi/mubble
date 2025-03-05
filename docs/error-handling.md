# Error Handling

This document explains how to handle errors in Mubble bots.

## Overview

Error handling is a critical part of building robust Telegram bots. Mubble provides several mechanisms for handling errors at different levels:

1. **Handler-level error handling**: Try-except blocks in individual handlers
2. **Middleware-based error handling**: Middleware that catches and processes errors
3. **Global error handlers**: Centralized error handling for all updates
4. **Result types**: Using `Result` and `Option` types for safe error handling

## Handler-Level Error Handling

The simplest way to handle errors is to use try-except blocks in your handlers:

```python
from mubble import Message
from mubble.modules import logger

@bot.on.message()
async def handler(message: Message) -> None:
    try:
        # Potentially risky operation
        result = perform_operation()
        await message.answer(f"Operation result: {result}")
    except Exception as e:
        logger.error("Error in handler: {}", e)
        await message.answer("Sorry, an error occurred while processing your request.")
```

This approach is straightforward but requires adding error handling code to each handler.

## Middleware-Based Error Handling

A more centralized approach is to use middleware for error handling:

```python
from mubble import Update, Context
from mubble.modules import logger

@bot.dispatch.middleware
async def error_middleware(update: Update, next_handler: Callable, ctx: Context) -> Any:
    try:
        # Call the next handler
        return await next_handler(update)
    except Exception as e:
        # Log the error
        logger.error("Error processing update: {}", e)
        
        # Notify the user
        if update.message:
            await update.message.answer("An error occurred while processing your request.")
        elif update.callback_query:
            await update.callback_query.answer("An error occurred while processing your request.", show_alert=True)
        
        # Prevent the error from propagating further
        return None
```

This middleware catches any exceptions thrown by handlers and provides a centralized place for error handling logic.

## Global Error Handlers

Mubble allows you to register global error handlers that will be called when an error occurs during update processing:

```python
from mubble import Update
from mubble.modules import logger

@bot.dispatch.error_handler
async def global_error_handler(update: Update, error: Exception) -> None:
    # Log the error
    logger.error("Error processing update {}: {}", update.update_id, error)
    
    # Notify the user
    if update.message:
        await update.message.answer(f"An error occurred: {type(error).__name__}")
    elif update.callback_query:
        await update.callback_query.answer(f"An error occurred: {type(error).__name__}", show_alert=True)
```

You can register multiple error handlers, which will be called in the order they were registered:

```python
@bot.dispatch.error_handler
async def log_error_handler(update: Update, error: Exception) -> None:
    # Log the error
    logger.error("Error processing update {}: {}", update.update_id, error)

@bot.dispatch.error_handler
async def notify_user_error_handler(update: Update, error: Exception) -> None:
    # Notify the user
    if update.message:
        await update.message.answer(f"An error occurred: {type(error).__name__}")
    elif update.callback_query:
        await update.callback_query.answer(f"An error occurred: {type(error).__name__}", show_alert=True)

@bot.dispatch.error_handler
async def notify_admin_error_handler(update: Update, error: Exception) -> None:
    # Notify the admin
    error_message = f"Error processing update {update.update_id}: {error}"
    await bot.api.send_message(chat_id=ADMIN_CHAT_ID, text=error_message)
```

## Using Result and Option Types

Mubble provides `Result` and `Option` types for safe error handling, inspired by Rust's error handling model:

### Result Type

The `Result` type represents either a successful value (`Ok`) or an error (`Err`):

```python
from mubble import Result, Ok, Err

def divide(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Err("Division by zero")
    return Ok(a / b)

# Using the Result
result = divide(10, 2)
if result.is_ok():
    value = result.unwrap()  # Safe because we checked is_ok()
    print(f"Result: {value}")
else:
    error = result.unwrap_err()
    print(f"Error: {error}")

# Pattern matching
match divide(10, 0):
    case Ok(value):
        print(f"Result: {value}")
    case Err(error):
        print(f"Error: {error}")

# Using map and map_err
result = divide(10, 2).map(lambda x: x * 2).map_err(lambda e: f"Error: {e}")

# Using and_then for chaining operations
def sqrt(x: float) -> Result[float, str]:
    if x < 0:
        return Err("Cannot take square root of negative number")
    return Ok(x ** 0.5)

result = divide(10, 2).and_then(sqrt)
```

### Option Type

The `Option` type represents either a value (`Some`) or no value (`None`):

```python
from mubble import Option, Some, NoneType

def find_user(user_id: int) -> Option[User]:
    user = database.get_user(user_id)
    if user:
        return Some(user)
    return NoneType()

# Using the Option
option = find_user(123)
if option.is_some():
    user = option.unwrap()  # Safe because we checked is_some()
    print(f"User: {user.name}")
else:
    print("User not found")

# Pattern matching
match find_user(123):
    case Some(user):
        print(f"User: {user.name}")
    case NoneType():
        print("User not found")

# Using map
option = find_user(123).map(lambda user: user.name)

# Using and_then for chaining operations
def find_user_posts(user: User) -> Option[List[Post]]:
    posts = database.get_user_posts(user.id)
    if posts:
        return Some(posts)
    return NoneType()

option = find_user(123).and_then(find_user_posts)
```

### Using Result with API Calls

Mubble's API client methods return `Result` types:

```python
from mubble import API, Token

api = API(token=Token("YOUR_BOT_TOKEN"))

async def send_message_safely(chat_id: int, text: str) -> None:
    result = await api.send_message(chat_id=chat_id, text=text)
    
    if result.is_ok():
        message = result.unwrap()
        print(f"Message sent: {message.message_id}")
    else:
        error = result.unwrap_err()
        print(f"Failed to send message: {error}")

# Or using pattern matching
async def send_message_safely(chat_id: int, text: str) -> None:
    match await api.send_message(chat_id=chat_id, text=text):
        case Ok(message):
            print(f"Message sent: {message.message_id}")
        case Err(error):
            print(f"Failed to send message: {error}")
```

## Error Handling Patterns

### Retrying Operations

```python
from mubble import Result, Ok, Err
import asyncio

async def retry_operation(operation: Callable, max_retries: int = 3, delay: float = 1.0) -> Result:
    retries = 0
    while retries < max_retries:
        result = await operation()
        if result.is_ok():
            return result
        
        retries += 1
        if retries < max_retries:
            await asyncio.sleep(delay)
    
    return result  # Return the last error result

# Usage
async def send_message() -> Result:
    return await api.send_message(chat_id=chat_id, text=text)

result = await retry_operation(send_message)
```

### Fallback Values

```python
from mubble import Result, Ok, Err

def get_user_setting(user_id: int, setting_name: str, default_value: Any) -> Any:
    result = database.get_setting(user_id, setting_name)
    return result.unwrap_or(default_value)

# Usage
language = get_user_setting(user_id, "language", "en")
```

### Logging and Continuing

```python
from mubble import Result, Ok, Err
from mubble.modules import logger

async def process_updates(updates: List[Update]) -> None:
    for update in updates:
        result = await process_update(update)
        if result.is_err():
            error = result.unwrap_err()
            logger.error("Error processing update {}: {}", update.update_id, error)
            # Continue processing other updates
```

### Structured Error Handling

```python
from mubble import Result, Ok, Err
from dataclasses import dataclass

@dataclass
class ValidationError:
    field: str
    message: str

@dataclass
class DatabaseError:
    code: int
    message: str

def validate_user(user_data: dict) -> Result[User, ValidationError]:
    if "name" not in user_data:
        return Err(ValidationError(field="name", message="Name is required"))
    if "email" not in user_data:
        return Err(ValidationError(field="email", message="Email is required"))
    return Ok(User(name=user_data["name"], email=user_data["email"]))

def save_user(user: User) -> Result[User, DatabaseError]:
    try:
        user_id = database.save_user(user)
        user.id = user_id
        return Ok(user)
    except Exception as e:
        return Err(DatabaseError(code=500, message=str(e)))

# Usage
async def create_user_handler(message: Message) -> None:
    user_data = {"name": "John Doe"}
    
    match validate_user(user_data):
        case Ok(user):
            match save_user(user):
                case Ok(saved_user):
                    await message.answer(f"User created: {saved_user.id}")
                case Err(error):
                    await message.answer(f"Database error: {error.message}")
        case Err(error):
            await message.answer(f"Validation error: {error.field} - {error.message}")
```

## Best Practices

### Be Specific About Exceptions

Catch specific exceptions rather than using a broad `except Exception` clause:

```python
try:
    # Operation that might raise different exceptions
    result = perform_operation()
except ValueError as e:
    # Handle value errors
    logger.error("Invalid value: {}", e)
except IOError as e:
    # Handle I/O errors
    logger.error("I/O error: {}", e)
except Exception as e:
    # Handle other exceptions
    logger.error("Unexpected error: {}", e)
```

### Log Detailed Error Information

Include as much context as possible in error logs:

```python
try:
    result = perform_operation(user_id, data)
except Exception as e:
    logger.error(
        "Error in perform_operation: user_id={}, data={}, error={}",
        user_id,
        data,
        e,
        exc_info=True  # Include traceback
    )
```

### Provide Helpful Error Messages to Users

Give users actionable information without exposing sensitive details:

```python
try:
    result = perform_operation(user_id, data)
except ValueError:
    await message.answer("Please provide valid input.")
except PermissionError:
    await message.answer("You don't have permission to perform this action.")
except Exception as e:
    # Log the detailed error
    logger.error("Unexpected error: {}", e, exc_info=True)
    # Provide a generic message to the user
    await message.answer("An unexpected error occurred. Please try again later.")
```

### Use Context for Error Handling

Store error handling information in the context:

```python
@bot.dispatch.middleware
async def error_context_middleware(update: Update, next_handler: Callable, ctx: Context) -> Any:
    # Set up error handling context
    ctx.set("errors", [])
    
    # Call the next handler
    result = await next_handler(update)
    
    # Check if there were errors
    errors = ctx.get("errors")
    if errors:
        # Handle errors
        if update.message:
            error_messages = "\n".join(errors)
            await update.message.answer(f"Errors occurred:\n{error_messages}")
    
    return result

# In a handler
@bot.on.message()
async def handler(message: Message, ctx: Context) -> None:
    try:
        result = perform_operation()
    except Exception as e:
        # Add error to context
        errors = ctx.get("errors", [])
        errors.append(str(e))
        ctx.set("errors", errors)
        
        # Continue execution
```

### Graceful Degradation

Design your bot to continue functioning even when some features fail:

```python
@bot.on.message(Command("weather"))
async def weather_handler(message: Message) -> None:
    try:
        weather_data = await get_weather_data(message.text)
        await message.answer(format_weather(weather_data))
    except Exception as e:
        logger.error("Weather service error: {}", e)
        # Fallback to a simpler response
        await message.answer(
            "Sorry, I couldn't get the weather information right now. "
            "Please try again later or check another service."
        )
```

## Next Steps

Now that you understand error handling in Mubble, you can explore:

- [Middleware](middleware.md)
- [State Management](state-management.md)
- [Handlers](handlers.md)
- [Rules](rules.md) 