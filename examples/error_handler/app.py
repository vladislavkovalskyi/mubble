import typing

from mubble_old import API, Message, Mubble, ParseMode, Token
from mubble_old.modules import logger
from mubble_old.rules import Markup

api = API(token=Token.from_env())
bot = Mubble(api)
logger.set_level("INFO")


@bot.on.message(
    Markup(
        [
            "/solve <a:int> <(+-/*)^operator> <b:int>",
            "/solve <a:int><(+-/*)^operator><b:int>",
        ]
    )
)
async def solve(
    message: Message,
    a: int,
    b: int,
    operator: typing.Literal["+", "-", "/", "*"],
):
    statement = f"{a} {operator} {b}"
    await message.reply(
        f"🤓 Result: <code>{statement} = {eval(statement):.2f}</code>",
        parse_mode=ParseMode.HTML,
    )


@solve.error_handler(ZeroDivisionError)
async def zero_division_catcher(_: ZeroDivisionError) -> str:
    return f"🤓 Error: you can't divide by zero! {_}"


bot.run_forever()
