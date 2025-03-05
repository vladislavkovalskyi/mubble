# Global Context

This document explains how to use the global context in Mubble for sharing data across updates.

## Overview

The global context in Mubble provides a way to store and access data that persists across different updates. Unlike the regular context, which is created for each update and discarded afterward, the global context is shared across all updates processed by the bot.

The global context is useful for:

1. **Storing Application State**: Keeping track of application-wide state
2. **Sharing Resources**: Sharing database connections, API clients, and other resources
3. **Caching Data**: Storing frequently accessed data to improve performance
4. **Configuration**: Storing configuration values that are used throughout the application

## Basic Usage

### Accessing the Global Context

You can access the global context through the regular context object:

```python
from mubble import Message, Context

@bot.on.message()
async def handler(message: Message, ctx: Context) -> None:
    # Get the global context
    global_ctx = ctx.global_ctx
    
    # Use the global context
    counter = global_ctx.get("counter", 0)
    counter += 1
    global_ctx.set("counter", counter)
    
    await message.answer(f"This message has been processed {counter} times.")
```

### Setting and Getting Values

You can set and get values in the global context:

```python
from mubble import Message, Context

@bot.on.message()
async def handler(message: Message, ctx: Context) -> None:
    # Get the global context
    global_ctx = ctx.global_ctx
    
    # Set a value
    global_ctx.set("last_user", message.from_user.id)
    
    # Get a value
    last_user = global_ctx.get("last_user")
    
    # Get a value with a default
    counter = global_ctx.get("counter", 0)
    
    # Check if a key exists
    has_counter = "counter" in global_ctx
    
    # Delete a key
    if "temporary_data" in global_ctx:
        del global_ctx["temporary_data"]
    
    await message.answer(f"Last user: {last_user}, Counter: {counter}")
```

### Using Context Variables

You can use context variables for type-safe access to the global context:

```python
from mubble import Message, Context, ContextVar

# Define context variables
counter_var = ContextVar[int]("counter")
last_user_var = ContextVar[int]("last_user")

@bot.on.message()
async def handler(message: Message, ctx: Context) -> None:
    # Get the global context
    global_ctx = ctx.global_ctx
    
    # Set values using context variables
    counter = counter_var.get(global_ctx, 0)  # Get with default value
    counter += 1
    counter_var.set(global_ctx, counter)
    
    last_user_var.set(global_ctx, message.from_user.id)
    
    # Get values using context variables
    last_user = last_user_var.get(global_ctx)
    
    await message.answer(f"Last user: {last_user}, Counter: {counter}")
```

## Advanced Usage

### Storing Complex Objects

You can store complex objects in the global context:

```python
from mubble import Message, Context
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class UserStats:
    message_count: int = 0
    command_count: int = 0
    last_activity: float = 0

# Initialize the global context
@bot.dispatch.middleware
async def init_global_context(update, next_handler, ctx: Context):
    global_ctx = ctx.global_ctx
    
    # Initialize user stats if not exists
    if "user_stats" not in global_ctx:
        global_ctx.set("user_stats", {})
    
    return await next_handler(update)

@bot.on.message()
async def message_handler(message: Message, ctx: Context) -> None:
    global_ctx = ctx.global_ctx
    user_stats: Dict[int, UserStats] = global_ctx.get("user_stats")
    
    # Get or create user stats
    user_id = message.from_user.id
    if user_id not in user_stats:
        user_stats[user_id] = UserStats()
    
    # Update user stats
    user_stats[user_id].message_count += 1
    user_stats[user_id].last_activity = time.time()
    
    # Check if it's a command
    if message.text and message.text.startswith("/"):
        user_stats[user_id].command_count += 1
    
    # Store updated user stats
    global_ctx.set("user_stats", user_stats)
    
    # Get user stats
    stats = user_stats[user_id]
    await message.answer(
        f"Your stats:\n"
        f"Messages: {stats.message_count}\n"
        f"Commands: {stats.command_count}"
    )
```

### Thread Safety

The global context is thread-safe, so you can use it safely in a multi-threaded environment:

```python
import threading
from mubble import Message, Context

@bot.on.message()
async def handler(message: Message, ctx: Context) -> None:
    global_ctx = ctx.global_ctx
    
    # Thread-safe operations
    counter = global_ctx.get("counter", 0)
    counter += 1
    global_ctx.set("counter", counter)
    
    await message.answer(f"Counter: {counter}")

# You can also access the global context from a background thread
def background_task(global_ctx):
    while True:
        # Thread-safe operations
        counter = global_ctx.get("counter", 0)
        print(f"Current counter: {counter}")
        time.sleep(60)

# Start the background thread
threading.Thread(
    target=background_task,
    args=(bot.global_ctx,),
    daemon=True
).start()
```

### Initialization and Cleanup

You can initialize the global context when the bot starts and clean it up when the bot stops:

```python
from mubble import API, Mubble, Token
import asyncio

# Create API client and bot
api = API(token=Token("YOUR_BOT_TOKEN"))
bot = Mubble(api)

# Initialize the global context
async def init_global_context():
    # Set initial values
    bot.global_ctx.set("start_time", time.time())
    bot.global_ctx.set("counter", 0)
    bot.global_ctx.set("user_stats", {})
    
    print("Global context initialized")

# Clean up the global context
async def cleanup_global_context():
    # Perform cleanup
    if "user_stats" in bot.global_ctx:
        # Save user stats to a database
        user_stats = bot.global_ctx.get("user_stats")
        await save_user_stats_to_db(user_stats)
    
    print("Global context cleaned up")

# Register your handlers
@bot.on.message()
async def handler(message, ctx):
    # Use the global context
    global_ctx = ctx.global_ctx
    counter = global_ctx.get("counter", 0)
    counter += 1
    global_ctx.set("counter", counter)
    
    await message.answer(f"Counter: {counter}")

# Run the bot
async def main():
    # Initialize the global context
    await init_global_context()
    
    try:
        # Start the bot
        await bot.start_polling()
    finally:
        # Clean up the global context
        await cleanup_global_context()

if __name__ == "__main__":
    asyncio.run(main())
```

### Using with Dependency Injection

You can use the global context for dependency injection:

```python
from mubble import Message, Context
import aiohttp
import motor.motor_asyncio

# Initialize the global context with dependencies
@bot.dispatch.middleware
async def init_dependencies(update, next_handler, ctx: Context):
    global_ctx = ctx.global_ctx
    
    # Initialize HTTP session if not exists
    if "http_session" not in global_ctx:
        global_ctx.set("http_session", aiohttp.ClientSession())
    
    # Initialize database client if not exists
    if "db_client" not in global_ctx:
        client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
        global_ctx.set("db_client", client)
        global_ctx.set("db", client.my_database)
    
    return await next_handler(update)

# Clean up dependencies
async def cleanup_dependencies():
    global_ctx = bot.global_ctx
    
    # Close HTTP session
    if "http_session" in global_ctx:
        session = global_ctx.get("http_session")
        await session.close()
    
    # Close database client
    if "db_client" in global_ctx:
        client = global_ctx.get("db_client")
        client.close()

# Use dependencies in handlers
@bot.on.message()
async def handler(message: Message, ctx: Context) -> None:
    global_ctx = ctx.global_ctx
    
    # Get HTTP session
    session = global_ctx.get("http_session")
    
    # Get database
    db = global_ctx.get("db")
    
    # Use the dependencies
    async with session.get("https://api.example.com/data") as response:
        data = await response.json()
    
    await db.users.update_one(
        {"user_id": message.from_user.id},
        {"$set": {"last_activity": time.time()}}
    )
    
    await message.answer(f"Data: {data}")
```

## Context Variables

### Defining Context Variables

You can define context variables for type-safe access to the global context:

```python
from mubble import ContextVar
from typing import Dict, List, Optional

# Define context variables
counter_var = ContextVar[int]("counter")
user_stats_var = ContextVar[Dict[int, UserStats]]("user_stats")
http_session_var = ContextVar[aiohttp.ClientSession]("http_session")
db_var = ContextVar[motor.motor_asyncio.AsyncIOMotorDatabase]("db")
```

### Using Context Variables

You can use context variables to get and set values in the global context:

```python
from mubble import Message, Context

@bot.on.message()
async def handler(message: Message, ctx: Context) -> None:
    global_ctx = ctx.global_ctx
    
    # Get values using context variables
    counter = counter_var.get(global_ctx, 0)  # Get with default value
    user_stats = user_stats_var.get(global_ctx, {})
    session = http_session_var.get(global_ctx)
    db = db_var.get(global_ctx)
    
    # Set values using context variables
    counter += 1
    counter_var.set(global_ctx, counter)
    
    # Use the values
    await message.answer(f"Counter: {counter}")
```

### Optional Context Variables

You can define optional context variables:

```python
from mubble import ContextVar
from typing import Optional

# Define an optional context variable
optional_var = ContextVar[Optional[str]]("optional_value")

@bot.on.message()
async def handler(message: Message, ctx: Context) -> None:
    global_ctx = ctx.global_ctx
    
    # Get the optional value
    optional_value = optional_var.get(global_ctx)
    
    if optional_value is None:
        await message.answer("Optional value is not set")
    else:
        await message.answer(f"Optional value: {optional_value}")
```

## Best Practices

### Use for Shared Resources

Use the global context for resources that need to be shared across handlers:

```python
from mubble import Message, Context
import aiohttp

@bot.dispatch.middleware
async def init_http_session(update, next_handler, ctx: Context):
    global_ctx = ctx.global_ctx
    
    # Initialize HTTP session if not exists
    if "http_session" not in global_ctx:
        global_ctx.set("http_session", aiohttp.ClientSession())
    
    return await next_handler(update)

@bot.on.message()
async def handler(message: Message, ctx: Context) -> None:
    global_ctx = ctx.global_ctx
    
    # Get HTTP session
    session = global_ctx.get("http_session")
    
    # Use the session
    async with session.get("https://api.example.com/data") as response:
        data = await response.json()
    
    await message.answer(f"Data: {data}")
```

### Clean Up Resources

Always clean up resources stored in the global context:

```python
from mubble import API, Mubble, Token
import asyncio
import aiohttp

# Create API client and bot
api = API(token=Token("YOUR_BOT_TOKEN"))
bot = Mubble(api)

# Initialize the global context
@bot.dispatch.middleware
async def init_http_session(update, next_handler, ctx: Context):
    global_ctx = ctx.global_ctx
    
    # Initialize HTTP session if not exists
    if "http_session" not in global_ctx:
        global_ctx.set("http_session", aiohttp.ClientSession())
    
    return await next_handler(update)

# Clean up resources
async def cleanup_resources():
    global_ctx = bot.global_ctx
    
    # Close HTTP session
    if "http_session" in global_ctx:
        session = global_ctx.get("http_session")
        await session.close()

# Run the bot
async def main():
    try:
        # Start the bot
        await bot.start_polling()
    finally:
        # Clean up resources
        await cleanup_resources()

if __name__ == "__main__":
    asyncio.run(main())
```

### Use Context Variables for Type Safety

Use context variables for type-safe access to the global context:

```python
from mubble import ContextVar
import aiohttp

# Define context variables
http_session_var = ContextVar[aiohttp.ClientSession]("http_session")

@bot.on.message()
async def handler(message: Message, ctx: Context) -> None:
    global_ctx = ctx.global_ctx
    
    # Get HTTP session using context variable
    session = http_session_var.get(global_ctx)
    
    # Use the session
    async with session.get("https://api.example.com/data") as response:
        data = await response.json()
    
    await message.answer(f"Data: {data}")
```

### Avoid Storing Large Data

Avoid storing large amounts of data in the global context:

```python
from mubble import Message, Context

@bot.on.message()
async def handler(message: Message, ctx: Context) -> None:
    global_ctx = ctx.global_ctx
    
    # BAD: Storing large data in the global context
    if "large_data" not in global_ctx:
        large_data = load_large_data()  # This loads a large dataset
        global_ctx.set("large_data", large_data)
    
    # GOOD: Storing a reference to the data
    if "data_loader" not in global_ctx:
        data_loader = DataLoader()  # This is a lightweight object
        global_ctx.set("data_loader", data_loader)
    
    # Use the data loader to get the data when needed
    data_loader = global_ctx.get("data_loader")
    data = data_loader.get_data()
    
    await message.answer(f"Data size: {len(data)}")
```

### Use for Configuration

Use the global context for configuration values:

```python
from mubble import Message, Context

# Initialize configuration
@bot.dispatch.middleware
async def init_config(update, next_handler, ctx: Context):
    global_ctx = ctx.global_ctx
    
    # Set configuration values if not exists
    if "config" not in global_ctx:
        config = {
            "api_url": "https://api.example.com",
            "api_key": "your-api-key",
            "max_retries": 3,
            "timeout": 10
        }
        global_ctx.set("config", config)
    
    return await next_handler(update)

@bot.on.message()
async def handler(message: Message, ctx: Context) -> None:
    global_ctx = ctx.global_ctx
    
    # Get configuration
    config = global_ctx.get("config")
    
    # Use configuration values
    api_url = config["api_url"]
    api_key = config["api_key"]
    
    await message.answer(f"API URL: {api_url}")
```

## Next Steps

Now that you understand the global context in Mubble, you can explore:

- [State Management](state-management.md)
- [Context](context.md)
- [Middleware](middleware.md)
- [Handlers](handlers.md) 