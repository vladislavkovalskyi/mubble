import typing

from fntypes.result import Error

from mubble.api.abc import ABCAPI
from mubble.bot.cute_types import BaseCute
from mubble.bot.dispatch.context import Context
from mubble.modules import logger
from mubble.tools.i18n.base import I18nEnum
from mubble.types import Update

from .middleware.abc import ABCMiddleware
from .return_manager.abc import ABCReturnManager

if typing.TYPE_CHECKING:
    from mubble.bot.dispatch.handler.abc import ABCHandler
    from mubble.bot.rules.abc import ABCRule

T = typing.TypeVar("T", bound=BaseCute)
_: typing.TypeAlias = typing.Any


async def process_inner(
    event: T,
    raw_event: Update,
    middlewares: list[ABCMiddleware[T]],
    handlers: list["ABCHandler[T]"],
    return_manager: ABCReturnManager[T],
) -> bool:
    logger.debug("Processing {!r}...", event.__class__.__name__)
    ctx = Context(raw_update=raw_event)

    for middleware in middlewares:
        if await middleware.pre(event, ctx) is False:
            return False

    found = False
    responses = []
    ctx_copy = ctx.copy()

    for handler in handlers:
        if await handler.check(event.api, raw_event, ctx):
            found = True
            response = await handler.run(event, ctx)
            responses.append(response)
            await return_manager.run(response, event, ctx)
            if handler.is_blocking:
                break
            ctx = ctx_copy

    for middleware in middlewares:
        await middleware.post(event, responses, ctx)

    return found


async def check_rule(
    api: ABCAPI,
    rule: "ABCRule",
    update: Update,
    ctx: Context,
) -> bool:
    """Checks requirements, adapts update.
    Returns check result."""

    cute_model = await rule.adapter.adapt(api, update)
    match cute_model:
        case Error(err):
            logger.debug("Adapter failed with error message: {!r}", str(err))
            return False

    ctx_copy = ctx.copy()
    for requirement in rule.requires:
        if not await check_rule(api, requirement, update, ctx_copy):
            return False

    ctx |= ctx_copy

    if I18nEnum.I18N in ctx:
        rule = await rule.translate(ctx.get(I18nEnum.I18N))

    return await rule.check(cute_model.unwrap(), ctx)


__all__ = ("check_rule", "process_inner")
