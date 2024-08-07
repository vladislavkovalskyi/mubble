import typing

import vbml

from mubble.bot.dispatch.context import Context
from mubble.node.text import Text
from mubble.tools.global_context.mubble_ctx import MubbleContext

from .abc import ABCRule

PatternLike: typing.TypeAlias = str | vbml.Pattern
global_ctx = MubbleContext()


def check_string(patterns: list[vbml.Pattern], s: str, ctx: Context) -> bool:
    for pattern in patterns:
        match global_ctx.vbml_patcher.check(pattern, s):
            case None | False:
                continue
            case {**response}:
                ctx |= response
        return True
    return False


class Markup(ABCRule):
    def __init__(self, patterns: PatternLike | list[PatternLike], /):
        if not isinstance(patterns, list):
            patterns = [patterns]
        self.patterns = [
            vbml.Pattern(pattern) if isinstance(pattern, str) else pattern
            for pattern in patterns
        ]

    async def check(self, text: Text, ctx: Context) -> bool:
        return check_string(self.patterns, text, ctx)


__all__ = ("Markup", "check_string")
