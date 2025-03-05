# Rules

Rules in Mubble are conditions that determine when handlers should be executed. This document explains how to use and create rules.

## Overview

Rules are a powerful feature of Mubble that allow you to filter updates and route them to the appropriate handlers. They can be based on message content, user properties, chat types, and more.

## Built-in Rules

Mubble provides many built-in rules for common use cases:

### Text Rules

#### Text

Matches messages with specific text:

```python
from mubble.rules import Text

@bot.on.message(Text("Hello"))
async def hello_handler(message: Message) -> None:
    await message.answer("Hello to you too!")

# Match multiple texts
@bot.on.message(Text(["Hello", "Hi", "Hey"]))
async def greeting_handler(message: Message) -> None:
    await message.answer("Greetings!")
```

#### Regex

Matches messages using regular expressions:

```python
from mubble.rules import Regex

@bot.on.message(Regex(r"^\d+$"))
async def number_handler(message: Message) -> None:
    await message.answer(f"You sent a number: {message.text}")

# With capture groups
@bot.on.message(Regex(r"^(\d+)\+(\d+)$"))
async def addition_handler(message: Message, match: re.Match) -> None:
    a, b = map(int, match.groups())
    await message.answer(f"{a} + {b} = {a + b}")
```

### Command Rules

#### Command

Matches command messages:

```python
from mubble.rules import Command

@bot.on.message(Command("help"))
async def help_handler(message: Message) -> None:
    await message.answer("This is the help message.")

# With arguments
@bot.on.message(Command("echo"))
async def echo_handler(message: Message) -> None:
    args = message.text.split()[1:]  # Get arguments after command
    await message.answer(" ".join(args))
```

#### StartCommand

Specialized rule for the `/start` command:

```python
from mubble.rules import StartCommand

@bot.on.message(StartCommand())
async def start_handler(message: Message) -> None:
    await message.answer("Welcome to the bot!")

# With parameter extraction
@bot.on.message(StartCommand(lambda x: int(x) if x.isdigit() else None))
async def start_with_param(message: Message, param: int | None) -> None:
    if param is None:
        await message.answer("Started without a parameter")
    else:
        await message.answer(f"Started with parameter: {param}")
```

### Markup Rules

The `Markup` rule allows you to define patterns with parameter extraction:

```python
from mubble.rules import Markup

@bot.on.message(Markup(["/random <a:int> <b:int>"]))
async def random_handler(message: Message, a: int, b: int) -> None:
    import random
    await message.answer(f"Random number between {a} and {b}: {random.randint(a, b)}")
```

### Callback Query Rules

#### CallbackQueryEq

Matches callback queries with specific data:

```python
from mubble import CallbackQuery

@bot.on.callback_query(lambda cq: cq.data == "option_1")
async def option_1_handler(callback_query: CallbackQuery) -> None:
    await callback_query.answer("You selected Option 1!")
```

#### PayloadEqRule

Matches callback queries with specific payload:

```python
from mubble.rules import PayloadEqRule

@bot.on.callback_query(PayloadEqRule("confirm/action"))
async def confirm_handler(callback_query: CallbackQuery) -> None:
    await callback_query.answer("Action confirmed!")
```

#### PayloadMarkupRule

Extracts parameters from callback query data:

```python
from mubble.rules import PayloadMarkupRule

@bot.on.callback_query(PayloadMarkupRule("number/<n:int>"))
async def number_handler(callback_query: CallbackQuery, n: int) -> None:
    await callback_query.answer(f"You selected number {n}")
```

#### PayloadModelRule

Deserializes callback query data into a model:

```python
import dataclasses
from mubble.rules import PayloadModelRule
from mubble.tools.callback_data_serilization import MsgPackSerializer

@dataclasses.dataclass(slots=True, frozen=True)
class Item:
    __key__ = "item"
    name: str
    amount: int = dataclasses.field(kw_only=True)

@bot.on.callback_query(
    PayloadModelRule(Item, serializer=MsgPackSerializer, alias="item")
)
async def item_handler(callback_query: CallbackQuery, item: Item) -> None:
    await callback_query.answer(f"Selected {item.name} (${item.amount})")
```

### User and Chat Rules

#### FromUser

Matches messages from specific users:

```python
from mubble.rules import FromUser

@bot.on.message(FromUser(123456789))
async def admin_handler(message: Message) -> None:
    await message.answer("Hello, admin!")

# Multiple users
@bot.on.message(FromUser([123456789, 987654321]))
async def vip_handler(message: Message) -> None:
    await message.answer("Hello, VIP user!")
```

#### ChatTypeRule

Matches messages from specific chat types:

```python
from mubble.rules import ChatTypeRule
from mubble.types.enums import ChatType

@bot.on.message(ChatTypeRule(ChatType.PRIVATE))
async def private_handler(message: Message) -> None:
    await message.answer("This is a private chat")

@bot.on.message(ChatTypeRule(ChatType.GROUP))
async def group_handler(message: Message) -> None:
    await message.answer("This is a group chat")
```

## Combining Rules

You can combine rules using logical operators:

### AND

```python
from mubble.rules import Text, FromUser

@bot.on.message(Text("admin") & FromUser(123456789))
async def admin_command_handler(message: Message) -> None:
    await message.answer("Admin command executed")
```

### OR

```python
from mubble.rules import Text

@bot.on.message(Text("hello") | Text("hi"))
async def greeting_handler(message: Message) -> None:
    await message.answer("Greetings!")
```

### NOT

```python
from mubble.rules import FromUser

@bot.on.message(~FromUser(123456789))
async def non_admin_handler(message: Message) -> None:
    await message.answer("You're not the admin")
```

## Custom Rules

You can create custom rules by implementing the `ABCRule` interface:

```python
from mubble import ABCRule, Message, Context

class HasPhotoRule(ABCRule[Message]):
    async def check(self, event: Message, ctx: Context) -> bool:
        return bool(event.photo)

@bot.on.message(HasPhotoRule())
async def photo_handler(message: Message) -> None:
    await message.answer("Nice photo!")
```

### Rules with Parameters

You can create rules that extract parameters:

```python
from mubble import ABCRule, Message, Context
import re

class NumberRule(ABCRule[Message]):
    def __init__(self) -> None:
        self.pattern = re.compile(r"^(\d+)$")
    
    async def check(self, event: Message, ctx: Context) -> bool:
        if not event.text:
            return False
        
        match = self.pattern.match(event.text)
        if match:
            ctx.set("number", int(match.group(1)))
            return True
        return False

@bot.on.message(NumberRule())
async def number_handler(message: Message, ctx: Context) -> None:
    number = ctx.get("number")
    await message.answer(f"You sent the number: {number}")
```

## Next Steps

Now that you understand rules, you can explore:

- [Handlers](handlers.md)
- [Dispatching](dispatching.md)
- [Context](global-context.md)
- [Callback Queries](callback-queries.md) 