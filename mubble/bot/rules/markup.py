import typing

import vbml

from mubble.bot.dispatch.context import Context
from mubble.tools.global_context import MubbleCtx

from .abc import Message
from .text import TextMessageRule

PatternLike: typing.TypeAlias = str | vbml.Pattern
global_ctx = MubbleCtx()


def check_string(patterns: list[vbml.Pattern], s: str, ctx: Context) -> bool:
    for pattern in patterns:
        match global_ctx.vbml_patcher.check(pattern, s):
            case None | False:
                continue
            case {**response}:
                ctx |= response
        return True
    return False


class Markup(TextMessageRule):
    def __init__(self, patterns: PatternLike | list[PatternLike], /):
        if not isinstance(patterns, list):
            patterns = [patterns]
        self.patterns = [
            vbml.Pattern(pattern) if isinstance(pattern, str) else pattern
            for pattern in patterns
        ]

    async def check(self, message: Message, ctx: Context) -> bool:
        return check_string(self.patterns, message.text.unwrap(), ctx)


__all__ = ("Markup", "check_string")
