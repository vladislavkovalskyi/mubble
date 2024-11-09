from mubble_old import Token, API, Mubble
from mubble_old.modules import logger

api = API(Token.from_env())
bot = Mubble(api)
logger.set_level("INFO")


@bot.loop_wrapper.timer(seconds=5)
async def once():
    print("I only fire once after startup, and that's it.")


@bot.loop_wrapper.interval(minutes=1)
async def repeat():
    print("I kick in every minute.")


@bot.loop_wrapper.lifespan.on_startup
async def startup():
    print("I'm working on startup.")


@bot.loop_wrapper.lifespan.on_shutdown
async def shutdown():
    print("I'm working on shutdown.")


bot.run_forever()
