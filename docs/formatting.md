# Formatting

This document explains how to format messages in Mubble for Telegram bots.

## Overview

Telegram supports several formatting options for messages:

1. **Markdown**: Simple formatting with limited features
2. **HTML**: More formatting options but requires proper HTML syntax
3. **Entities**: Programmatic formatting with precise control

Mubble provides convenient methods to work with all these formatting options.

## Basic Formatting

### Markdown Formatting

Markdown is the simplest way to format messages:

```python
from mubble import Message, ParseMode

@bot.on.message()
async def handler(message: Message) -> None:
    # Send a message with Markdown formatting
    await message.answer(
        "Hello, *bold text*, _italic text_, `code`, "
        "[inline URL](https://example.com)",
        parse_mode=ParseMode.MARKDOWN
    )
```

Supported Markdown syntax:
- `*bold*`: **bold text**
- `_italic_`: _italic text_
- `` `code` ``: `code`
- `[text](URL)`: [text](URL)

### HTML Formatting

HTML provides more formatting options:

```python
from mubble import Message, ParseMode

@bot.on.message()
async def handler(message: Message) -> None:
    # Send a message with HTML formatting
    await message.answer(
        "Hello, <b>bold text</b>, <i>italic text</i>, <code>code</code>, "
        "<a href='https://example.com'>inline URL</a>, "
        "<s>strikethrough</s>, <u>underline</u>, "
        "<pre>pre-formatted fixed-width code block</pre>, "
        "<blockquote>blockquote</blockquote>",
        parse_mode=ParseMode.HTML
    )
```

Supported HTML tags:
- `<b>...</b>` or `<strong>...</strong>`: **bold text**
- `<i>...</i>` or `<em>...</em>`: _italic text_
- `<u>...</u>`: underlined text
- `<s>...</s>` or `<strike>...</strike>` or `<del>...</del>`: strikethrough text
- `<code>...</code>`: inline code
- `<pre>...</pre>`: pre-formatted fixed-width code block
- `<a href="...">...</a>`: inline link
- `<blockquote>...</blockquote>`: blockquote

### Escaping Special Characters

When using formatting, you need to escape special characters:

```python
from mubble import Message, ParseMode
import html

@bot.on.message()
async def handler(message: Message) -> None:
    # Escape special characters for HTML
    user_input = html.escape(message.text)
    await message.answer(
        f"You said: <b>{user_input}</b>",
        parse_mode=ParseMode.HTML
    )
```

For Markdown, you need to escape these characters: `_`, `*`, `` ` ``, `[`:

```python
from mubble import Message, ParseMode
import re

def escape_markdown(text: str) -> str:
    """Escape Markdown special characters."""
    return re.sub(r"([_*\[\]`])", r"\\\1", text)

@bot.on.message()
async def handler(message: Message) -> None:
    # Escape special characters for Markdown
    user_input = escape_markdown(message.text)
    await message.answer(
        f"You said: *{user_input}*",
        parse_mode=ParseMode.MARKDOWN
    )
```

## Advanced Formatting

### Entities

For more precise control over formatting, you can use message entities:

```python
from mubble import Message, MessageEntity, EntityType

@bot.on.message()
async def handler(message: Message) -> None:
    # Create a message with entities
    text = "Hello, this is bold and this is italic."
    entities = [
        MessageEntity(
            type=EntityType.BOLD,
            offset=7,
            length=9
        ),
        MessageEntity(
            type=EntityType.ITALIC,
            offset=21,
            length=10
        )
    ]
    
    # Send the message with entities
    await message.answer(text, entities=entities)
```

Available entity types:
- `EntityType.BOLD`: Bold text
- `EntityType.ITALIC`: Italic text
- `EntityType.UNDERLINE`: Underlined text
- `EntityType.STRIKETHROUGH`: Strikethrough text
- `EntityType.CODE`: Inline code
- `EntityType.PRE`: Pre-formatted code block
- `EntityType.TEXT_LINK`: Text link (requires `url` parameter)
- `EntityType.MENTION`: Mention (@username)
- `EntityType.HASHTAG`: Hashtag (#hashtag)
- `EntityType.CASHTAG`: Cashtag ($USD)
- `EntityType.BOT_COMMAND`: Bot command (/start)
- `EntityType.URL`: URL
- `EntityType.EMAIL`: Email
- `EntityType.PHONE_NUMBER`: Phone number
- `EntityType.CUSTOM_EMOJI`: Custom emoji (requires `custom_emoji_id` parameter)

### Code Blocks with Language Syntax Highlighting

You can create code blocks with syntax highlighting:

```python
from mubble import Message, ParseMode

@bot.on.message()
async def handler(message: Message) -> None:
    # HTML code block with syntax highlighting
    code = """
def hello_world():
    print("Hello, world!")
    
hello_world()
    """
    
    await message.answer(
        f"<pre><code class='language-python'>{html.escape(code)}</code></pre>",
        parse_mode=ParseMode.HTML
    )
    
    # Markdown code block with syntax highlighting
    await message.answer(
        f"```python\n{code}\n```",
        parse_mode=ParseMode.MARKDOWN_V2
    )
```

### Markdown V2

Telegram also supports an extended version of Markdown called MarkdownV2:

```python
from mubble import Message, ParseMode

@bot.on.message()
async def handler(message: Message) -> None:
    # Send a message with MarkdownV2 formatting
    await message.answer(
        "Hello, *bold text*, _italic text_, __underline__, ~strikethrough~, "
        "`code`, ```python\ndef hello():\n    print('Hello')\n```, "
        "[inline URL](https://example.com)",
        parse_mode=ParseMode.MARKDOWN_V2
    )
```

Supported MarkdownV2 syntax:
- `*bold*`: **bold text**
- `_italic_`: _italic text_
- `__underline__`: underlined text
- `~strikethrough~`: strikethrough text
- `` `code` ``: `code`
- `` ```language\ncode\n``` ``: code block with optional language syntax highlighting
- `[text](URL)`: [text](URL)

In MarkdownV2, you need to escape these characters: `_`, `*`, `[`, `]`, `(`, `)`, `~`, `` ` ``, `>`, `#`, `+`, `-`, `=`, `|`, `{`, `}`, `.`, `!`:

```python
from mubble import Message, ParseMode
import re

def escape_markdown_v2(text: str) -> str:
    """Escape MarkdownV2 special characters."""
    return re.sub(r"([_*\[\]()~`>#+\-=|{}.!])", r"\\\1", text)

@bot.on.message()
async def handler(message: Message) -> None:
    # Escape special characters for MarkdownV2
    user_input = escape_markdown_v2(message.text)
    await message.answer(
        f"You said: *{user_input}*",
        parse_mode=ParseMode.MARKDOWN_V2
    )
```

## Formatting Helpers

### Text Builder

Mubble provides a `TextBuilder` class to help build formatted messages:

```python
from mubble import Message, TextBuilder

@bot.on.message()
async def handler(message: Message) -> None:
    # Create a text builder
    builder = TextBuilder()
    
    # Add formatted text
    builder.add("Hello, ").bold("bold text").add(", ")
    builder.italic("italic text").add(", ")
    builder.code("code").add(", ")
    builder.link("inline URL", "https://example.com").add(", ")
    builder.strikethrough("strikethrough").add(", ")
    builder.underline("underline").add(".")
    
    # Send the message
    await message.answer(builder.text, entities=builder.entities)
```

### Formatting Functions

You can also use formatting functions:

```python
from mubble import Message, format_text, bold, italic, code, link

@bot.on.message()
async def handler(message: Message) -> None:
    # Format text using functions
    text, entities = format_text(
        "Hello, ",
        bold("bold text"),
        ", ",
        italic("italic text"),
        ", ",
        code("code"),
        ", ",
        link("inline URL", "https://example.com"),
        "."
    )
    
    # Send the message
    await message.answer(text, entities=entities)
```

## Working with User Input

### Preserving User Formatting

You can preserve the formatting from user messages:

```python
from mubble import Message

@bot.on.message()
async def handler(message: Message) -> None:
    # Get the user's message text and entities
    text = message.text
    entities = message.entities
    
    # Send the message with the same formatting
    await message.answer(f"You said: {text}", entities=entities)
```

### Extracting Formatted Parts

You can extract parts of a formatted message:

```python
from mubble import Message, EntityType

@bot.on.message()
async def handler(message: Message) -> None:
    # Extract all URLs from the message
    urls = []
    if message.entities:
        for entity in message.entities:
            if entity.type == EntityType.URL or entity.type == EntityType.TEXT_LINK:
                start = entity.offset
                end = entity.offset + entity.length
                url_text = message.text[start:end]
                
                if entity.type == EntityType.TEXT_LINK:
                    urls.append(entity.url)
                else:
                    urls.append(url_text)
    
    # Reply with the extracted URLs
    if urls:
        await message.answer(f"Found URLs: {', '.join(urls)}")
    else:
        await message.answer("No URLs found in your message.")
```

## Formatting Media Captions

You can also format captions for media messages:

```python
from mubble import Message, ParseMode

@bot.on.message()
async def handler(message: Message) -> None:
    # Send a photo with a formatted caption
    await message.answer_photo(
        photo="https://example.com/image.jpg",
        caption="Photo with *bold* and _italic_ caption",
        parse_mode=ParseMode.MARKDOWN
    )
```

## Formatting Buttons

You can format text in inline keyboard buttons:

```python
from mubble import Message, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode

@bot.on.message()
async def handler(message: Message) -> None:
    # Create an inline keyboard with formatted button text
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Bold Button",
                    callback_data="bold"
                ),
                InlineKeyboardButton(
                    text="Italic Button",
                    callback_data="italic"
                )
            ]
        ]
    )
    
    # Send a message with the keyboard
    await message.answer(
        "Choose a formatting option:",
        reply_markup=keyboard
    )

@bot.on.callback_query(PayloadEqRule("bold"))
async def bold_callback(callback_query):
    await callback_query.message.edit_text(
        "*This text is bold*",
        parse_mode=ParseMode.MARKDOWN
    )

@bot.on.callback_query(PayloadEqRule("italic"))
async def italic_callback(callback_query):
    await callback_query.message.edit_text(
        "_This text is italic_",
        parse_mode=ParseMode.MARKDOWN
    )
```

## Best Practices

### Choose the Right Format

- Use **Markdown** for simple formatting needs
- Use **HTML** for more complex formatting
- Use **Entities** for precise control or when you need to manipulate formatting programmatically

### Handle User Input Safely

Always escape user input to prevent formatting injection:

```python
from mubble import Message, ParseMode
import html

@bot.on.message()
async def handler(message: Message) -> None:
    # Safely include user input in formatted messages
    user_input = html.escape(message.text)
    await message.answer(
        f"<b>You said:</b> {user_input}",
        parse_mode=ParseMode.HTML
    )
```

### Test Your Formatting

Test your formatting on different platforms (mobile, desktop, web) to ensure it looks good everywhere.

### Keep It Readable

Don't overuse formatting. Keep your messages clean and readable.

### Use Consistent Formatting

Use consistent formatting throughout your bot for a better user experience.

## Next Steps

Now that you understand formatting in Mubble, you can explore:

- [Inline Keyboards](inline-keyboards.md)
- [Callback Queries](callback-queries.md)
- [Internationalization](i18n.md)
- [Handlers](handlers.md) 