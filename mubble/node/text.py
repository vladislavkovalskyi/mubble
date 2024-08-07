from mubble.node.base import ComposeError, ScalarNode
from mubble.node.message import MessageNode


class Text(ScalarNode, str):
    @classmethod
    async def compose(cls, message: MessageNode) -> str:
        if not message.text:
            raise ComposeError("Message has no text")
        return message.text.unwrap()


class TextInteger(ScalarNode, int):
    @classmethod
    async def compose(cls, text: Text) -> int:
        if not text.isdigit():
            raise ComposeError("Text is not digit")
        return int(text)


__all__ = ("Text", "TextInteger")
