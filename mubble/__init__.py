"""Mubble

Mubble is a next-generation framework known for its great speed and simplicity. It is written using aiohttp, asyncio, and msgspec.

* Written on Python
* Asynchronous and very fast.

Basic example:

```python

from mubble import API, Message, Mubble, Token
from mubble.modules import logger
from mubble.rules import Text

api = API(token=Token("123:ABC"))
bot = Mubble(api)
logger.set_level("INFO")


@bot.on.message(Text("/start"))
async def start(message: Message):
    me = (await api.get_me()).unwrap()
    await message.answer(
        f"Hello, {message.from_user.full_name}! I'm {me.full_name}."
    )

bot.run_forever()
```
"""

import typing

from .api import API, APIError, APIResponse, Token
from .bot import (
    ABCDispatch,
    ABCHandler,
    ABCMiddleware,
    ABCPolling,
    ABCReturnManager,
    ABCRule,
    ABCScenario,
    ABCStateView,
    ABCView,
    BaseCute,
    BaseReturnManager,
    BaseStateView,
    BaseView,
    CallbackQueryCute,
    CallbackQueryReturnManager,
    CallbackQueryRule,
    CallbackQueryView,
    ChatJoinRequestCute,
    ChatJoinRequestRule,
    ChatJoinRequestView,
    ChatMemberUpdatedCute,
    ChatMemberView,
    Checkbox,
    Choice,
    Dispatch,
    FuncHandler,
    InlineQueryCute,
    InlineQueryReturnManager,
    InlineQueryRule,
    MessageCute,
    MessageReplyHandler,
    MessageReturnManager,
    MessageRule,
    MessageView,
    Polling,
    RawEventView,
    ShortState,
    Mubble,
    UpdateCute,
    ViewBox,
    WaiterMachine,
    register_manager,
)
from .client import ABCClient, AiohttpClient
from .model import Model
from .modules import logger
from .tools import (
    ABCErrorHandler,
    ABCGlobalContext,
    ABCLoopWrapper,
    ABCTranslator,
    ABCTranslatorMiddleware,
    AnyMarkup,
    Button,
    CtxVar,
    DelayedTask,
    ErrorHandler,
    FormatString,
    GlobalContext,
    HTMLFormatter,
    I18nEnum,
    InlineButton,
    InlineKeyboard,
    Keyboard,
    KeyboardSetBase,
    KeyboardSetYAML,
    Lifespan,
    LoopWrapper,
    ParseMode,
    RowButtons,
    SimpleI18n,
    SimpleTranslator,
    ctx_var,
    magic_bundle,
)

Update: typing.TypeAlias = UpdateCute
Message: typing.TypeAlias = MessageCute
ChatJoinRequest: typing.TypeAlias = ChatJoinRequestCute
ChatMemberUpdated: typing.TypeAlias = ChatMemberUpdatedCute
CallbackQuery: typing.TypeAlias = CallbackQueryCute
InlineQuery: typing.TypeAlias = InlineQueryCute
Bot: typing.TypeAlias = Mubble


__all__ = (
    "API",
    "ABCClient",
    "ABCDispatch",
    "ABCErrorHandler",
    "ABCGlobalContext",
    "ABCHandler",
    "ABCLoopWrapper",
    "ABCMiddleware",
    "ABCPolling",
    "ABCReturnManager",
    "ABCRule",
    "ABCScenario",
    "ABCStateView",
    "ABCTranslator",
    "ABCTranslatorMiddleware",
    "ABCView",
    "API",
    "APIError",
    "APIResponse",
    "AiohttpClient",
    "AnyMarkup",
    "BaseCute",
    "BaseReturnManager",
    "BaseStateView",
    "BaseView",
    "Bot",
    "Button",
    "CallbackQuery",
    "CallbackQueryCute",
    "CallbackQueryReturnManager",
    "CallbackQueryView",
    "ChatJoinRequest",
    "ChatJoinRequestCute",
    "CallbackQueryRule",
    "ChatJoinRequestRule",
    "InlineQueryRule",
    "ChatJoinRequestView",
    "ChatMemberUpdated",
    "ChatMemberUpdatedCute",
    "ChatMemberView",
    "Checkbox",
    "CtxVar",
    "DelayedTask",
    "Dispatch",
    "ErrorHandler",
    "FormatString",
    "FuncHandler",
    "GlobalContext",
    "HTMLFormatter",
    "I18nEnum",
    "InlineButton",
    "InlineKeyboard",
    "InlineQuery",
    "InlineQueryCute",
    "InlineQueryReturnManager",
    "Keyboard",
    "KeyboardSetBase",
    "KeyboardSetYAML",
    "Lifespan",
    "LoopWrapper",
    "Message",
    "MessageCute",
    "MessageReplyHandler",
    "MessageReturnManager",
    "MessageRule",
    "MessageView",
    "Model",
    "ParseMode",
    "Polling",
    "RawEventView",
    "RowButtons",
    "ShortState",
    "SimpleI18n",
    "SimpleTranslator",
    "Choice",
    "Mubble",
    "Token",
    "Update",
    "UpdateCute",
    "ViewBox",
    "WaiterMachine",
    "ctx_var",
    "logger",
    "magic_bundle",
    "register_manager",
)
