import typing

import vbml

from mubble.tools.global_context import GlobalContext, ctx_var


class MubbleCtx(GlobalContext):
    """Basic type-hinted mubble context with context name `"mubble"`.

    You can use this class or GlobalContext:
    ```
    from mubble.tools.global_context import GlobalContext, MubbleCtx

    ctx1 = MubbleCtx()
    ctx2 = GlobalContext("mubble")  # same, but without the type-hints
    assert ctx1 == ctx2  # ok
    ```"""

    __ctx_name__ = "mubble"

    vbml_patcher: typing.ClassVar[vbml.Patcher] = ctx_var(vbml.Patcher(), const=True)


__all__ = ("MubbleCtx",)
