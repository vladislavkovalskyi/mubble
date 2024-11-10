from mubble import API, Mubble, Token
from mubble.modules import logger
from mubble.rules import PaymentInvoiceCurrency
from mubble.types.enums import Currency

bot = Mubble(API(Token.from_env()))


@bot.on.pre_checkout_query(PaymentInvoiceCurrency(Currency.UAH))
async def handle_invoice_telegram_stars(_) -> bool:
    logger.info("Invoice detected!")
    return True


bot.run_forever()
