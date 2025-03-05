# Loop Wrapper

This document explains how to use the loop wrapper in Mubble for managing the asyncio event loop.

## Overview

The loop wrapper in Mubble provides a convenient way to manage the asyncio event loop when running your bot. It handles:

1. **Loop Creation**: Creating and configuring the asyncio event loop
2. **Task Management**: Managing tasks running in the event loop
3. **Graceful Shutdown**: Properly shutting down the bot when receiving termination signals
4. **Error Handling**: Handling exceptions in the event loop

## Basic Usage

### Running a Bot with the Loop Wrapper

The simplest way to use the loop wrapper is with the `run_polling` method:

```python
from mubble import API, Mubble, Token

# Create API client and bot
api = API(token=Token("YOUR_BOT_TOKEN"))
bot = Mubble(api)

# Register your handlers
@bot.on.message()
async def echo_handler(message):
    await message.answer(message.text)

# Run the bot with polling
if __name__ == "__main__":
    bot.run_polling()
```

This method:
1. Creates an asyncio event loop
2. Starts the bot in polling mode
3. Handles termination signals (SIGINT, SIGTERM)
4. Properly shuts down the bot when terminated

### Running a Bot with a Custom Loop

You can also use the loop wrapper with a custom event loop:

```python
import asyncio
from mubble import API, Mubble, Token
from mubble.loop import LoopWrapper

# Create API client and bot
api = API(token=Token("YOUR_BOT_TOKEN"))
bot = Mubble(api)

# Register your handlers
@bot.on.message()
async def echo_handler(message):
    await message.answer(message.text)

# Create a custom event loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Create a loop wrapper
wrapper = LoopWrapper(loop=loop)

# Run the bot with the loop wrapper
if __name__ == "__main__":
    wrapper.run(bot.start_polling())
```

## Advanced Usage

### Running Multiple Tasks

You can run multiple tasks in the event loop:

```python
import asyncio
from mubble import API, Mubble, Token
from mubble.loop import LoopWrapper

# Create API client and bot
api = API(token=Token("YOUR_BOT_TOKEN"))
bot = Mubble(api)

# Register your handlers
@bot.on.message()
async def echo_handler(message):
    await message.answer(message.text)

# Define a background task
async def background_task():
    while True:
        print("Background task running...")
        await asyncio.sleep(60)

# Create a loop wrapper
wrapper = LoopWrapper()

# Run the bot and background task
if __name__ == "__main__":
    wrapper.run(
        bot.start_polling(),
        background_task()
    )
```

### Custom Shutdown Handlers

You can add custom shutdown handlers to perform cleanup when the bot is shutting down:

```python
import asyncio
from mubble import API, Mubble, Token
from mubble.loop import LoopWrapper

# Create API client and bot
api = API(token=Token("YOUR_BOT_TOKEN"))
bot = Mubble(api)

# Register your handlers
@bot.on.message()
async def echo_handler(message):
    await message.answer(message.text)

# Define a shutdown handler
async def on_shutdown():
    print("Bot is shutting down...")
    # Perform cleanup tasks
    await asyncio.sleep(1)
    print("Cleanup completed.")

# Create a loop wrapper with a shutdown handler
wrapper = LoopWrapper(on_shutdown=on_shutdown)

# Run the bot
if __name__ == "__main__":
    wrapper.run(bot.start_polling())
```

### Custom Signal Handlers

You can customize how the loop wrapper handles signals:

```python
import asyncio
import signal
from mubble import API, Mubble, Token
from mubble.loop import LoopWrapper

# Create API client and bot
api = API(token=Token("YOUR_BOT_TOKEN"))
bot = Mubble(api)

# Register your handlers
@bot.on.message()
async def echo_handler(message):
    await message.answer(message.text)

# Define a custom signal handler
def custom_signal_handler(signum, frame):
    print(f"Received signal {signum}")
    # Perform custom signal handling

# Create a loop wrapper
wrapper = LoopWrapper()

# Register custom signal handlers
signal.signal(signal.SIGINT, custom_signal_handler)
signal.signal(signal.SIGTERM, custom_signal_handler)

# Run the bot
if __name__ == "__main__":
    wrapper.run(bot.start_polling())
```

### Error Handling

The loop wrapper handles exceptions in the event loop:

```python
import asyncio
from mubble import API, Mubble, Token
from mubble.loop import LoopWrapper

# Create API client and bot
api = API(token=Token("YOUR_BOT_TOKEN"))
bot = Mubble(api)

# Register your handlers
@bot.on.message()
async def echo_handler(message):
    await message.answer(message.text)

# Define a task that raises an exception
async def error_task():
    await asyncio.sleep(5)
    raise ValueError("This is a test error")

# Define an error handler
def error_handler(loop, context):
    exception = context.get("exception")
    print(f"Error in event loop: {exception}")
    # Log the error, notify administrators, etc.

# Create a loop wrapper with an error handler
loop = asyncio.new_event_loop()
loop.set_exception_handler(error_handler)
wrapper = LoopWrapper(loop=loop)

# Run the bot and error task
if __name__ == "__main__":
    wrapper.run(
        bot.start_polling(),
        error_task()
    )
```

## Integration with Web Frameworks

### Using with AIOHTTP

You can integrate the loop wrapper with AIOHTTP:

```python
import asyncio
from aiohttp import web
from mubble import API, Mubble, Token, WebhookConfig
from mubble.server import setup_webhook
from mubble.loop import LoopWrapper

# Create API client and bot
api = API(token=Token("YOUR_BOT_TOKEN"))
bot = Mubble(api)

# Register your handlers
@bot.on.message()
async def echo_handler(message):
    await message.answer(message.text)

# Configure webhook
webhook_config = WebhookConfig(
    url="https://your-domain.com/webhook",
    secret_token="your-secret-token"
)

# Create AIOHTTP application
app = web.Application()

# Add your routes
app.router.add_get("/", lambda request: web.Response(text="Bot is running"))

# Setup webhook
setup_webhook(
    app=app,
    bot=bot,
    webhook_config=webhook_config,
    path="/webhook"
)

# Define startup and shutdown handlers
async def on_startup(app):
    # Set webhook
    await api.set_webhook(webhook_config)
    print("Webhook set")

async def on_shutdown(app):
    # Delete webhook
    await api.delete_webhook()
    print("Webhook deleted")

# Register startup and shutdown handlers
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

# Create a loop wrapper
wrapper = LoopWrapper()

# Run the application
if __name__ == "__main__":
    wrapper.run(web._run_app(app, host="0.0.0.0", port=8443))
```

### Using with FastAPI

You can integrate the loop wrapper with FastAPI:

```python
import asyncio
import uvicorn
from fastapi import FastAPI, Request, Response
from mubble import API, Mubble, Token, WebhookConfig
from mubble.server import process_update
from mubble.loop import LoopWrapper

# Create API client and bot
api = API(token=Token("YOUR_BOT_TOKEN"))
bot = Mubble(api)

# Register your handlers
@bot.on.message()
async def echo_handler(message):
    await message.answer(message.text)

# Configure webhook
webhook_config = WebhookConfig(
    url="https://your-domain.com/webhook",
    secret_token="your-secret-token"
)

# Create FastAPI application
app = FastAPI()

# Add webhook endpoint
@app.post("/webhook")
async def webhook(request: Request):
    # Verify secret token
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != webhook_config.secret_token:
        return Response(status_code=403)
    
    # Process update
    update_data = await request.json()
    await process_update(bot, update_data)
    
    return Response(status_code=200)

# Add startup event
@app.on_event("startup")
async def on_startup():
    # Set webhook
    await api.set_webhook(webhook_config)
    print("Webhook set")

# Add shutdown event
@app.on_event("shutdown")
async def on_shutdown():
    # Delete webhook
    await api.delete_webhook()
    print("Webhook deleted")

# Create a custom server class that uses the loop wrapper
class LoopWrapperUvicornServer(uvicorn.Server):
    def run(self, sockets=None):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        wrapper = LoopWrapper(loop=loop)
        wrapper.run(self.serve(sockets=sockets))

# Run the application
if __name__ == "__main__":
    config = uvicorn.Config(app, host="0.0.0.0", port=8443)
    server = LoopWrapperUvicornServer(config=config)
    server.run()
```

## Custom Loop Wrapper

You can create a custom loop wrapper by inheriting from the `LoopWrapper` class:

```python
import asyncio
import signal
import sys
from mubble.loop import LoopWrapper

class CustomLoopWrapper(LoopWrapper):
    def __init__(self, loop=None, on_shutdown=None):
        super().__init__(loop, on_shutdown)
        self.tasks = []
    
    def run(self, *coros):
        """Run the event loop with the given coroutines."""
        self.loop = self.loop or asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        # Create tasks
        self.tasks = [self.loop.create_task(coro) for coro in coros]
        
        # Set up signal handlers
        try:
            for sig in (signal.SIGINT, signal.SIGTERM):
                self.loop.add_signal_handler(sig, self._shutdown)
        except NotImplementedError:
            # Windows doesn't support add_signal_handler
            for sig in (signal.SIGINT, signal.SIGTERM):
                signal.signal(sig, self._shutdown_signal)
        
        # Run the event loop
        try:
            self.loop.run_forever()
        finally:
            self._cleanup()
    
    def _shutdown(self):
        """Shutdown the event loop."""
        print("Shutting down...")
        
        # Cancel all tasks
        for task in self.tasks:
            task.cancel()
        
        # Schedule the shutdown coroutine
        if self.on_shutdown:
            self.loop.create_task(self._shutdown_coro())
        else:
            self.loop.stop()
    
    async def _shutdown_coro(self):
        """Run the shutdown coroutine and stop the loop."""
        if self.on_shutdown:
            await self.on_shutdown()
        self.loop.stop()
    
    def _shutdown_signal(self, signum, frame):
        """Handle shutdown signal."""
        self._shutdown()
    
    def _cleanup(self):
        """Clean up the event loop."""
        try:
            # Cancel all tasks
            pending = asyncio.all_tasks(self.loop)
            for task in pending:
                task.cancel()
            
            # Run the event loop until all tasks are cancelled
            self.loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
            
            # Close the event loop
            self.loop.close()
        finally:
            asyncio.set_event_loop(None)
            sys.exit(0)
```

## Best Practices

### Use the Built-in Methods

For most use cases, the built-in `run_polling` method is sufficient:

```python
if __name__ == "__main__":
    bot.run_polling()
```

### Handle Graceful Shutdown

Always ensure your bot shuts down gracefully:

```python
async def on_shutdown():
    # Close database connections
    await db.close()
    
    # Cancel background tasks
    for task in background_tasks:
        task.cancel()
    
    # Log shutdown
    logger.info("Bot shut down gracefully")

wrapper = LoopWrapper(on_shutdown=on_shutdown)
```

### Use Error Handling

Set up proper error handling for the event loop:

```python
def error_handler(loop, context):
    exception = context.get("exception")
    logger.error(f"Error in event loop: {exception}")
    # Notify administrators, restart the bot, etc.

loop = asyncio.new_event_loop()
loop.set_exception_handler(error_handler)
wrapper = LoopWrapper(loop=loop)
```

### Manage Background Tasks

Keep track of background tasks and ensure they're properly cancelled on shutdown:

```python
background_tasks = []

async def start_background_tasks():
    # Create and store background tasks
    task1 = asyncio.create_task(background_task1())
    task2 = asyncio.create_task(background_task2())
    background_tasks.extend([task1, task2])

async def on_shutdown():
    # Cancel background tasks
    for task in background_tasks:
        task.cancel()
    
    # Wait for tasks to be cancelled
    await asyncio.gather(*background_tasks, return_exceptions=True)

wrapper = LoopWrapper(on_shutdown=on_shutdown)
wrapper.run(bot.start_polling(), start_background_tasks())
```

## Next Steps

Now that you understand the loop wrapper in Mubble, you can explore:

- [Webhooks](webhooks.md)
- [Error Handling](error-handling.md)
- [Middleware](middleware.md)
- [State Management](state-management.md) 