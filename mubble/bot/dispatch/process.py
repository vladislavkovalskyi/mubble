import typing

from .waiter import Waiter
from .middleware.abc import ABCMiddleware
from .handler.abc import ABCHandler
from mubble.types import Update
from mubble.modules import logger
from mubble.result import Error
from mubble.api.abc import ABCAPI

if typing.TYPE_CHECKING:
    from mubble.bot.rules.abc import ABCRule

T = typing.TypeVar("T")
E = typing.TypeVar("E")
_ = typing.Any


async def process_waiters(
    api: ABCAPI,
    waiters: dict[T, Waiter],
    key: T,
    event: E | None,
    raw_event: Update,
    str_handler: typing.Callable,
) -> bool:
    if key not in waiters:
        return False

    logger.debug(
        "Update {} found in waiter (key={})", event.__class__.__name__, str(key)
    )

    waiter = waiters[key]
    ctx = {}

    for rule in waiter.rules:
        if not await check_rule(api, rule, raw_event, ctx):
            if not waiter.default:
                return True
            elif isinstance(waiter.default, str):
                await str_handler(waiter.default)
            else:
                await waiter.default(event)
            return True

    logger.debug("Waiter set as ready")

    waiters.pop(key)
    setattr(waiter.event, "e", (event, ctx))
    waiter.event.set()
    return True


async def process_inner(
    event: T,
    raw_event: Update,
    middlewares: list[ABCMiddleware[T]],
    handlers: list[ABCHandler[T]],
) -> bool:
    logger.debug("Processing {}", event.__class__.__name__)
    ctx = {}

    for middleware in middlewares:
        if await middleware.pre(event, ctx) is False:
            return False

    found = False
    responses = []
    for handler in handlers:
        if await handler.check(event.api, raw_event):
            found = True
            handler.ctx |= ctx
            responses.append(await handler.run(event))
            if handler.is_blocking:
                break

    for middleware in middlewares:
        await middleware.post(event, responses, ctx)

    return found


async def check_rule(
    api: ABCAPI, rule: "ABCRule", update: Update, ctx: dict[str, _]
) -> bool:
    """Checks requirements, adapts update
    Returns check result"""

    ctx_copy = ctx.copy()

    model = await rule.adapter.adapt(api, update)
    match model:
        case Error(_):
            return False

    for requirement in rule.require:
        if not await check_rule(api, requirement, update, ctx_copy):
            return False

    ctx |= ctx_copy
    return await rule.check(model.unwrap(), ctx)
