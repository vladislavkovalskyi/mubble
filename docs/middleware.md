# Middleware

This document explains how to use middleware in Mubble to process updates before they reach handlers.

## Overview

Middleware in Mubble allows you to intercept and process updates before they reach handlers. This is useful for:

- Logging
- Authentication and authorization
- Rate limiting
- Preprocessing updates
- Error handling
- Internationalization

## Basic Usage

### Registering Middleware

You can register middleware using the `middleware` decorator on the dispatcher:

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

## Advanced Usage

### Context in Middleware

You can access and modify the context in middleware:

```python
from mubble import Context

@bot.dispatch.middleware
async def context_middleware(update: Update, next_handler: Callable, ctx: Context) -> Any:
    # Set data in context
    ctx.set("timestamp", time.time())
    
    # Call the next handler
    result = await next_handler(update)
    
    # Access data from context
    timestamp = ctx.get("timestamp")
    print(f"Processing time: {time.time() - timestamp} seconds")
    
    return result
```

### API Client in Middleware

You can access the API client in middleware:

```python
from mubble import API

@bot.dispatch.middleware
async def api_middleware(update: Update, next_handler: Callable, api: API) -> Any:
    # Use the API client
    me = (await api.get_me()).unwrap()
    print(f"Processing update for bot: {me.username}")
    
    # Call the next handler
    return await next_handler(update)
```

### Skipping Handlers

You can skip handlers in middleware:

```python
@bot.dispatch.middleware
async def auth_middleware(update: Update, next_handler: Callable, ctx: Context) -> Any:
    # Check if the user is authorized
    if update.message and update.message.from_user.id not in AUTHORIZED_USERS:
        # Skip handlers
        ctx.stop_propagation()
        
        # Send an unauthorized message
        await update.message.answer("You are not authorized to use this bot.")
        return None
    
    # Call the next handler
    return await next_handler(update)
```

### Modifying Updates

You can modify updates in middleware:

```python
@bot.dispatch.middleware
async def translation_middleware(update: Update, next_handler: Callable) -> Any:
    # Translate message text
    if update.message and update.message.text:
        original_text = update.message.text
        translated_text = translate(original_text)
        
        # Store the original text in a custom attribute
        update.message._original_text = original_text
        
        # Modify the text
        update.message.text = translated_text
    
    # Call the next handler
    return await next_handler(update)
```

## Common Middleware Patterns

### Logging Middleware

```python
from mubble.modules import logger

@bot.dispatch.middleware
async def logging_middleware(update: Update, next_handler: Callable) -> Any:
    # Log the incoming update
    logger.info(
        "Received update (update_id={}, type={})",
        update.update_id,
        update.update_type.name
    )
    
    # Log message details if present
    if update.message:
        logger.info(
            "Message from user {} (id={}): {}",
            update.message.from_user.full_name,
            update.message.from_user.id,
            update.message.text
        )
    
    # Call the next handler
    try:
        result = await next_handler(update)
        logger.info("Update processed successfully")
        return result
    except Exception as e:
        logger.error("Error processing update: {}", e)
        raise
```

### Rate Limiting Middleware

```python
import time
from collections import defaultdict

# Store last request time for each user
last_request = defaultdict(float)
# Rate limit: 1 request per second
RATE_LIMIT = 1.0

@bot.dispatch.middleware
async def rate_limit_middleware(update: Update, next_handler: Callable, ctx: Context) -> Any:
    # Get user ID
    user_id = None
    if update.message:
        user_id = update.message.from_user.id
    elif update.callback_query:
        user_id = update.callback_query.from_user.id
    
    if user_id:
        # Check if the user is rate limited
        current_time = time.time()
        time_since_last_request = current_time - last_request[user_id]
        
        if time_since_last_request < RATE_LIMIT:
            # User is rate limited
            ctx.stop_propagation()
            
            # Notify the user
            if update.message:
                await update.message.answer(
                    f"Please wait {RATE_LIMIT - time_since_last_request:.1f} seconds before sending another message."
                )
            elif update.callback_query:
                await update.callback_query.answer(
                    f"Please wait {RATE_LIMIT - time_since_last_request:.1f} seconds before clicking again.",
                    show_alert=True
                )
            
            return None
        
        # Update last request time
        last_request[user_id] = current_time
    
    # Call the next handler
    return await next_handler(update)
```

### Authentication Middleware

```python
# List of authorized user IDs
AUTHORIZED_USERS = [123456789, 987654321]

@bot.dispatch.middleware
async def auth_middleware(update: Update, next_handler: Callable, ctx: Context) -> Any:
    # Get user ID
    user_id = None
    if update.message:
        user_id = update.message.from_user.id
    elif update.callback_query:
        user_id = update.callback_query.from_user.id
    
    if user_id and user_id not in AUTHORIZED_USERS:
        # User is not authorized
        ctx.stop_propagation()
        
        # Notify the user
        if update.message:
            await update.message.answer("You are not authorized to use this bot.")
        elif update.callback_query:
            await update.callback_query.answer("You are not authorized to use this bot.", show_alert=True)
        
        return None
    
    # Call the next handler
    return await next_handler(update)
```

### Error Handling Middleware

```python
from mubble.modules import logger

@bot.dispatch.middleware
async def error_middleware(update: Update, next_handler: Callable) -> Any:
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
        
        # Optionally, re-raise the exception
        # raise
```

### Internationalization Middleware

```python
from mubble.tools.i18n import SimpleTranslator

# Create a translator
translator = SimpleTranslator(
    {
        "en": {
            "hello": "Hello, {}!",
            "welcome": "Welcome to the bot!"
        },
        "es": {
            "hello": "¡Hola, {}!",
            "welcome": "¡Bienvenido al bot!"
        }
    },
    default_locale="en"
)

@bot.dispatch.middleware
async def i18n_middleware(update: Update, next_handler: Callable, ctx: Context) -> Any:
    # Determine user's language
    user_language = "en"  # Default language
    
    if update.message and update.message.from_user.language_code:
        user_language = update.message.from_user.language_code
    
    # Set the language in context
    ctx.set("language", user_language)
    
    # Set the translator in context
    ctx.set("translator", translator)
    
    # Call the next handler
    return await next_handler(update)

# Use the translator in a handler
@bot.on.message(Text("/start"))
async def start_handler(message: Message, ctx: Context) -> None:
    # Get the translator and language from context
    translator = ctx.get("translator")
    language = ctx.get("language")
    
    # Translate the message
    welcome_message = translator.get("welcome", language)
    hello_message = translator.get("hello", language).format(message.from_user.first_name)
    
    await message.answer(f"{hello_message}\n{welcome_message}")
```

## Creating Middleware Classes

You can also create middleware classes by implementing the `ABCMiddleware` interface:

```python
from mubble import ABCMiddleware, Update

class LoggingMiddleware(ABCMiddleware):
    async def __call__(
        self, update: Update, next_handler: Callable, *args, **kwargs
    ) -> Any:
        # Pre-processing
        logger.info("Received update: {}", update.update_id)
        
        # Call the next handler
        try:
            result = await next_handler(update, *args, **kwargs)
            logger.info("Update processed successfully")
            return result
        except Exception as e:
            logger.error("Error processing update: {}", e)
            raise

# Register the middleware
bot.dispatch.middlewares.append(LoggingMiddleware())
```

## Best Practices

### Keep Middleware Focused

Each middleware should have a single responsibility. Instead of creating a single middleware that does many things, create multiple middleware functions that each do one thing well.

### Order Matters

The order in which middleware is registered matters. Middleware that should run first (e.g., authentication) should be registered first.

### Handle Errors

Make sure to handle errors in middleware, especially if the middleware is responsible for preprocessing updates.

### Be Careful with Modifications

If you modify updates in middleware, make sure to document this behavior and be aware of how it might affect handlers.

### Use Context for Sharing Data

Use the context object to share data between middleware and handlers.

## Next Steps

Now that you understand middleware, you can explore:

- [Handlers](handlers.md)
- [Rules](rules.md)
- [State Management](state-management.md)
- [Error Handling](error-handling.md) 