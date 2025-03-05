# State Management

This document explains how to manage state in Mubble bots, allowing you to create multi-step interactions and maintain context across messages.

## Overview

State management is essential for creating bots that can handle complex conversations and multi-step processes. Mubble provides several tools for managing state:

1. **Context**: For short-term state within a single update
2. **Global Context**: For state that persists across updates
3. **State Storage**: For long-term state persistence
4. **Short States**: For simple state machines

## Context

The `Context` object provides a way to store and retrieve data within a single update processing cycle:

```python
from mubble import Context, Message
from mubble.rules import Text

@bot.on.message(Text("/start"))
async def start_handler(message: Message, ctx: Context) -> None:
    # Store data in context
    ctx.set("user_id", message.from_user.id)
    
    # Retrieve data from context
    user_id = ctx.get("user_id")
    
    await message.answer(f"Your user ID is {user_id}")
```

The context is automatically injected into handlers that have a parameter of type `Context`.

### Context Propagation

Context is propagated through middleware and handlers:

```python
@bot.dispatch.middleware
async def middleware(update: Update, next_handler: Callable, ctx: Context) -> Any:
    # Set data in context
    ctx.set("timestamp", time.time())
    
    # Call the next handler (context will be passed along)
    return await next_handler(update)

@bot.on.message()
async def handler(message: Message, ctx: Context) -> None:
    # Access data set by middleware
    timestamp = ctx.get("timestamp")
    await message.answer(f"Received at {timestamp}")
```

### Stopping Propagation

You can use the context to stop the propagation of an update to other handlers:

```python
@bot.on.message(Text("/stop"), final=False)
async def stop_handler(message: Message, ctx: Context) -> None:
    await message.answer("Stopping propagation")
    
    # Stop propagation to other handlers
    ctx.stop_propagation()
```

## Global Context

The `GlobalContext` provides a way to store and retrieve data that persists across updates:

```python
from mubble.tools.global_context import GlobalContext

# Create a global context
global_context = GlobalContext()

# Use the global context in a handler
@bot.on.message(Text("/count"))
async def count_handler(message: Message) -> None:
    # Get the current count (default to 0 if not set)
    count = global_context.get("count", 0)
    
    # Increment the count
    count += 1
    
    # Store the new count
    global_context.set("count", count)
    
    await message.answer(f"Count: {count}")
```

### Context Variables

You can use context variables for more type-safe access to global context:

```python
from mubble.tools.global_context import ctx_var

# Define context variables
count_var = ctx_var("count", int, 0)  # Name, type, default value
user_ids_var = ctx_var("user_ids", set[int], set())

@bot.on.message(Text("/count"))
async def count_handler(message: Message) -> None:
    # Get the current count
    count = count_var.get()
    
    # Increment the count
    count += 1
    
    # Store the new count
    count_var.set(count)
    
    # Update user IDs
    user_ids = user_ids_var.get()
    user_ids.add(message.from_user.id)
    user_ids_var.set(user_ids)
    
    await message.answer(f"Count: {count}")
```

## State Storage

For long-term state persistence, Mubble provides the `StateStorage` interface:

```python
from mubble.tools.state_storage import MemoryStateStorage, StateData

# Create a memory-based state storage
state_storage = MemoryStateStorage()

@bot.on.message(Text("/save"))
async def save_handler(message: Message) -> None:
    user_id = message.from_user.id
    
    # Create state data
    state_data = StateData(
        state="waiting_for_name",
        data={"timestamp": time.time()}
    )
    
    # Save state for the user
    await state_storage.set(user_id, state_data)
    
    await message.answer("State saved. Please enter your name.")

@bot.on.message()
async def message_handler(message: Message) -> None:
    user_id = message.from_user.id
    
    # Get state for the user
    state_data = await state_storage.get(user_id)
    
    if state_data and state_data.state == "waiting_for_name":
        # Process the name
        name = message.text
        
        # Clear the state
        await state_storage.delete(user_id)
        
        # Get the timestamp from state data
        timestamp = state_data.data.get("timestamp")
        
        await message.answer(f"Hello, {name}! You started this conversation at {timestamp}.")
    else:
        await message.answer("I don't know what to do with this message.")
```

### Custom State Storage

You can implement your own state storage by inheriting from `ABCStateStorage`:

```python
from mubble.tools.state_storage import ABCStateStorage, StateData
import redis

class RedisStateStorage(ABCStateStorage):
    def __init__(self, redis_url: str) -> None:
        self.redis = redis.from_url(redis_url)
    
    async def get(self, key: str | int) -> StateData | None:
        data = self.redis.get(f"state:{key}")
        if data:
            return StateData.from_json(data)
        return None
    
    async def set(self, key: str | int, state_data: StateData) -> None:
        self.redis.set(f"state:{key}", state_data.to_json())
    
    async def delete(self, key: str | int) -> None:
        self.redis.delete(f"state:{key}")
```

## Short States

For simple state machines, Mubble provides the `ShortState` class:

```python
from mubble import ShortState, Message
from mubble.rules import Text

# Define states
START = ShortState("start")
WAITING_FOR_NAME = ShortState("waiting_for_name")
WAITING_FOR_AGE = ShortState("waiting_for_age")
FINISHED = ShortState("finished")

# Create a state storage
state_storage = MemoryStateStorage()

@bot.on.message(Text("/register"))
async def register_handler(message: Message) -> None:
    user_id = message.from_user.id
    
    # Set initial state
    await state_storage.set(user_id, StateData(state=START.state))
    
    # Transition to waiting for name
    await state_storage.set(user_id, StateData(state=WAITING_FOR_NAME.state))
    
    await message.answer("Please enter your name.")

@bot.on.message(WAITING_FOR_NAME)
async def name_handler(message: Message) -> None:
    user_id = message.from_user.id
    name = message.text
    
    # Store the name
    state_data = await state_storage.get(user_id)
    data = state_data.data or {}
    data["name"] = name
    
    # Transition to waiting for age
    await state_storage.set(
        user_id,
        StateData(state=WAITING_FOR_AGE.state, data=data)
    )
    
    await message.answer(f"Nice to meet you, {name}! Now, please enter your age.")

@bot.on.message(WAITING_FOR_AGE)
async def age_handler(message: Message) -> None:
    user_id = message.from_user.id
    
    try:
        age = int(message.text)
    except ValueError:
        await message.answer("Please enter a valid age (a number).")
        return
    
    # Get the stored data
    state_data = await state_storage.get(user_id)
    data = state_data.data or {}
    name = data.get("name", "User")
    
    # Store the age
    data["age"] = age
    
    # Transition to finished
    await state_storage.set(
        user_id,
        StateData(state=FINISHED.state, data=data)
    )
    
    await message.answer(f"Registration complete! Name: {name}, Age: {age}")
```

## State Views

For more complex state machines, you can use state views:

```python
from mubble import BaseStateView, Message, Context
from mubble.rules import Text

class RegistrationView(BaseStateView):
    def get_state_key(self, message: Message, ctx: Context) -> str:
        return str(message.from_user.id)
    
    @BaseStateView.state("start")
    async def start(self, message: Message) -> None:
        await message.answer("Please enter your name.")
        await self.set_state("waiting_for_name")
    
    @BaseStateView.state("waiting_for_name")
    async def waiting_for_name(self, message: Message) -> None:
        name = message.text
        await self.update_data(name=name)
        
        await message.answer(f"Nice to meet you, {name}! Now, please enter your age.")
        await self.set_state("waiting_for_age")
    
    @BaseStateView.state("waiting_for_age")
    async def waiting_for_age(self, message: Message) -> None:
        try:
            age = int(message.text)
        except ValueError:
            await message.answer("Please enter a valid age (a number).")
            return
        
        data = await self.get_data()
        name = data.get("name", "User")
        
        await self.update_data(age=age)
        
        await message.answer(f"Registration complete! Name: {name}, Age: {age}")
        await self.clear_state()

# Create the view
registration_view = RegistrationView(state_storage)

# Register the view
@bot.on.message(Text("/register"))
async def register_handler(message: Message) -> None:
    await registration_view.set_state("start", message)
    await registration_view.start(message)

# Register the view's message handler
@bot.on.message()
async def message_handler(message: Message) -> None:
    await registration_view.process_message(message)
```

## Best Practices

### Choose the Right State Management Tool

- Use `Context` for short-term state within a single update
- Use `GlobalContext` for application-wide state
- Use `StateStorage` for user-specific state that persists across updates
- Use `ShortState` for simple state machines
- Use state views for complex state machines

### Clean Up State

Always clean up state when it's no longer needed:

```python
# Clear state when a process is complete
await state_storage.delete(user_id)
```

### Handle Timeouts

Consider what happens if a user abandons a conversation:

```python
@bot.on.message(Text("/cancel"))
async def cancel_handler(message: Message) -> None:
    user_id = message.from_user.id
    
    # Clear the state
    await state_storage.delete(user_id)
    
    await message.answer("Operation cancelled.")
```

### Use Type-Safe State

Use type hints and validation to ensure state data is valid:

```python
from pydantic import BaseModel

class UserData(BaseModel):
    name: str
    age: int | None = None

@bot.on.message(WAITING_FOR_NAME)
async def name_handler(message: Message) -> None:
    user_id = message.from_user.id
    name = message.text
    
    # Create or update user data
    state_data = await state_storage.get(user_id)
    data = state_data.data or {}
    
    user_data = UserData(**data)
    user_data.name = name
    
    # Store the updated data
    await state_storage.set(
        user_id,
        StateData(state=WAITING_FOR_AGE.state, data=user_data.dict())
    )
    
    await message.answer(f"Nice to meet you, {name}! Now, please enter your age.")
```

## Next Steps

Now that you understand state management, you can explore:

- [Handlers](handlers.md)
- [Rules](rules.md)
- [Middleware](middleware.md)
- [Callback Queries](callback-queries.md) 