import inspect
import typing

from fntypes.option import Nothing, Option, Some
from fntypes.result import Error, Ok

from mubble.api.api import API
from mubble.bot.cute_types.update import UpdateCute
from mubble.bot.dispatch.context import Context
from mubble.bot.dispatch.middleware.abc import ABCMiddleware
from mubble.bot.dispatch.return_manager.abc import ABCReturnManager
from mubble.model import Model
from mubble.modules import logger
from mubble.node.composer import CONTEXT_STORE_NODES_KEY, NodeScope, compose_nodes
from mubble.tools.i18n.abc import I18nEnum
from mubble.types.objects import Update

if typing.TYPE_CHECKING:
    from mubble.bot.dispatch.handler.abc import ABCHandler
    from mubble.bot.rules.abc import ABCRule
    from mubble.bot.rules.adapter.abc import ABCAdapter


async def run_adapter[T](
    adapter: "ABCAdapter[Update, T]",
    api: API,
    update: Update,
    context: Context,
) -> Option[T]:
    adapt_result = adapter.adapt(api, update, context)
    match await adapt_result if inspect.isawaitable(adapt_result) else adapt_result:
        case Ok(value):
            return Some(value)
        case Error(err):
            logger.debug("Adapter failed with error message: {!r}", str(err))
            return Nothing()


async def process_inner[Event: Model](
    api: API,
    event: Event,
    raw_event: Update,
    middlewares: list[ABCMiddleware[Event]],
    handlers: list["ABCHandler[Event]"],
    return_manager: ABCReturnManager[Event] | None = None,
) -> bool:
    logger.debug("Processing {!r}...", event.__class__.__name__)
    ctx = Context(raw_update=raw_event)
    ctx[CONTEXT_STORE_NODES_KEY] = {}  # For per-event shared nodes

    logger.debug("Run pre middlewares...")
    for middleware in middlewares:
        if middleware.adapter is not None:
            match await run_adapter(middleware.adapter, api, raw_event, ctx):
                case Some(val):
                    event = val
                case Nothing():
                    return False

        middleware_result = await middleware.pre(event, ctx)
        logger.debug("Middleware {!r} returned: {!r}", middleware.__class__.__qualname__, middleware_result)
        if middleware_result is False:
            return False

    found = False
    responses = []
    ctx_copy = ctx.copy()

    for handler in handlers:
        if await handler.check(api, raw_event, ctx):
            logger.debug("Handler {!r} matched, run...", handler)
            found = True
            response = await handler.run(api, event, ctx)
            logger.debug("Handler {!r} returned: {!r}", handler, response)
            responses.append(response)
            if return_manager is not None:
                await return_manager.run(response, event, ctx)
            if handler.is_blocking:
                break

        ctx = ctx_copy

    logger.debug("Run post middlewares...")
    for middleware in middlewares:
        logger.debug("Run post middleware {!r}", middleware.__class__.__qualname__)
        await middleware.post(event, responses, ctx)

    for session in ctx.get(CONTEXT_STORE_NODES_KEY, {}).values():
        await session.close(scopes=(NodeScope.PER_EVENT,))

    logger.debug(
        "{} handlers, returns {!r}",
        "No found" if not found else "Found",
        found,
    )
    return found


async def check_rule(
    api: API,
    rule: "ABCRule",
    update: Update,
    ctx: Context,
) -> bool:
    """Checks requirements, adapts update.
    Returns check result."""

    update_cute = None if not isinstance(update, UpdateCute) else update

    # Running adapter
    match await run_adapter(rule.adapter, api, update, ctx):
        case Some(val):
            adapted_value = val
        case Nothing():
            return False

    # Preparing update
    if isinstance(adapted_value, UpdateCute):
        update_cute = adapted_value
    elif isinstance(adapted_val := ctx.get(rule.adapter.ADAPTED_VALUE_KEY or ""), UpdateCute):
        update_cute = adapted_val
    else:
        update_cute = UpdateCute.from_update(update, bound_api=api)

    # Running subrules to fetch requirements
    ctx_copy = ctx.copy()
    for requirement in rule.requires:
        if not await check_rule(api, requirement, update_cute, ctx_copy):
            return False

    # Translating translatable rules
    if I18nEnum.I18N in ctx:
        rule = await rule.translate(ctx[I18nEnum.I18N])

    ctx |= ctx_copy

    # Composing required nodes
    nodes = rule.required_nodes
    node_col = None
    if nodes:
        result = await compose_nodes(nodes, ctx, data={Update: update, API: api, UpdateCute: update_cute})
        if not result:
            return False
        node_col = result.value

    # Running check
    result = await rule.bounding_check(ctx, adapted_value=adapted_value, node_col=node_col)

    # Closing node sessions if there are any
    if node_col is not None:
        await node_col.close_all()

    return result


__all__ = ("check_rule", "process_inner")
