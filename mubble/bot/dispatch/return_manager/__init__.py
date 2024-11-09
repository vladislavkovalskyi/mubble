from mubble.bot.dispatch.return_manager.abc import (
    ABCReturnManager,
    BaseReturnManager,
    Manager,
    register_manager,
)
from mubble.bot.dispatch.return_manager.callback_query import CallbackQueryReturnManager
from mubble.bot.dispatch.return_manager.inline_query import InlineQueryReturnManager
from mubble.bot.dispatch.return_manager.message import MessageReturnManager
from mubble.bot.dispatch.return_manager.pre_checkout_query import PreCheckoutQueryManager

__all__ = (
    "ABCReturnManager",
    "BaseReturnManager",
    "CallbackQueryReturnManager",
    "InlineQueryReturnManager",
    "Manager",
    "MessageReturnManager",
    "PreCheckoutQueryManager",
    "register_manager",
)
