from mubble import API, Message, Mubble, Token
from mubble.modules import logger
from mubble.tools.parse_mode import ParseMode

logger.set_level("INFO")
api = API(Token.from_env())
api.default_params["parse_mode"] = ParseMode.HTML
bot = Mubble(api)


@bot.on.message()
async def forward_message(message: Message) -> str:
    result = (await message.forward(message.chat_id)).unwrap()
    forward_origin = result.forward_origin.unwrap().v
    text_response = (
        "⭐ Forwarded message detected!\n"
        "<blockquote>It was sent on <b>{}</b> from <i>{}</i>: <b>{}</b></blockquote>"
    ).format(forward_origin.date.ctime(), forward_origin.type, "{!r}")

    match forward_origin.type:
        case "chat":
            text_response = text_response.format(
                forward_origin.sender_chat,
            )
        case "channel":
            text_response = text_response.format(
                forward_origin.chat.title.unwrap(),
            )
        case "hidden_user":
            text_response = text_response.format(
                forward_origin.sender_user_name,
            )
        case "user":
            text_response = text_response.format(
                forward_origin.sender_user.full_name,
            )

    return text_response


bot.run_forever()
