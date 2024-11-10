from typing import Any

from mubble import API, Mubble, Token
from mubble.node.event import EventNode
from mubble.rules import Text
from mubble.types.enums import UpdateType
from mubble.types.objects import Message

bot = Mubble(API(Token.from_env()))


@bot.on(Text(["hello", "hi"], ignore_case=True))
async def handle_raw_message(raw_msg: EventNode[Message]) -> None:
    await bot.api.send_message(chat_id=raw_msg.chat_id, text="Hello, World!")


@bot.on(update_type=UpdateType.CALLBACK_QUERY)
async def handle_raw_callback(event: EventNode[dict[str, Any]]) -> None:
    await bot.api.answer_callback_query(callback_query_id=event["id"])


bot.run_forever()
