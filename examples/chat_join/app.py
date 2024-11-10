from fntypes.result import Error, Ok

from mubble import API, ChatJoinRequest, Mubble, Token
from mubble.rules import HasInviteLink, IsUser
from mubble.modules import logger

bot = Mubble(API(Token.from_env()))


@bot.on.chat_join_request(HasInviteLink(), IsUser())
async def new_user(request: ChatJoinRequest) -> None:
    match await request.approve():
        case Ok(ok) if ok:
            await request.ctx_api.send_message(
                chat_id=request.chat.id,
                text=(
                    f"😁 Welcome to {request.chat.title.unwrap()!r}"
                    f", {request.from_user.full_name}!"
                ),
            )
        case Error(error):
            logger.error(
                "Smth went wrong, error: {!r}, user: {}",
                error.error,
                request.from_user.full_name,
            )


bot.run_forever()
