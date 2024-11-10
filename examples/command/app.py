from mubble import API, Message, Mubble, Token
from mubble.modules import logger
from mubble.rules import Argument, Command

api = API(token=Token.from_env())
bot = Mubble(api)
logger.set_level("INFO")


def character(c: str) -> str | None:
    if len(c) != 1:
        return None
    return c


def sentence(s: str) -> str | None:
    if not s.startswith("'") and s.endswith("'"):
        return None
    s = s.removeprefix("'").removesuffix("'")
    return s


def int_validator(s: str) -> int | None:
    if not s.isdigit():
        return None
    return int(s)


# Try:
# /hide 'hello from mubble' _ 3
# /hide '0123456789' * 3
# /hide '#Mubble'
@bot.on.message(
    Command(
        "hide",
        Argument("string", [sentence]),
        Argument("char", [character], optional=True),
        Argument("count", [int_validator], optional=True),
    )
)
async def replace_handler(
    message: Message,
    string: str,
    char: str = "*",
    count: int = 1,
) -> None:
    logger.info("Received data: {}, {}, {}", string, char, count)
    await message.answer(f"🎮 Result: {(char * count) + string[count:]}")


@bot.on.message(
    Command(
        ["sum", "s"],
        Argument("x", [int_validator]),
        Argument("y", [int_validator]),
        Argument("z", [int_validator], optional=True),
    )
)
async def sum_handler(message: Message, x: int, y: int, z: int | None = None) -> str:
    logger.info("Received data: {}, {}, {}", x, y, z)
    await message.answer(f"🎮 Answer: {x + y + (z if z else 0)}")


bot.run_forever()
