from mubble_old import Token, API, Mubble
from mubble_old.bot.dispatch.handler import MessageReplyHandler
from mubble_old.modules import logger
from mubble_old.rules import Text

api = API(token=Token.from_env())
bot = Mubble(api)
logger.set_level("INFO")

phrases = [
    ("good morning", "Good morning!"),
    ("good bye", "Good bye!"),
    ("hello", "Hi!"),
    ("hi", "Hello!"),
]

bot.on.message.handlers.extend(
    [
        MessageReplyHandler(answer, Text(text, ignore_case=True))
        for text, answer in phrases
    ]
)


bot.run_forever()
