import dataclasses
import importlib
import typing

from mubble.bot.dispatch.context import Context
from mubble.node.base import ComposeError, Node
from mubble.node.update import UpdateNode

if typing.TYPE_CHECKING:
    from mubble.bot.dispatch.process import check_rule
    from mubble.bot.rules.abc import ABCRule


class RuleChain(dict[str, typing.Any]):
    dataclass = dict
    rules: tuple["ABCRule", ...] = ()

    def __init_subclass__(cls) -> None:
        if cls.__name__ == "_RuleNode":
            return
        cls.dataclass = cls.generate_node_dataclass(cls)

    def __new__(cls, *rules: "ABCRule") -> type[Node]:
        return type("_RuleNode", (cls,), {"dataclass": dict, "rules": rules})

    def __class_getitem__(
        cls, items: "ABCRule | tuple[ABCRule, ...]", /
    ) -> typing.Self:
        if not isinstance(items, tuple):
            items = (items,)
        assert all(
            isinstance(rule, "ABCRule") for rule in items
        ), "All items must be instances of 'ABCRule'."
        return cls(*items)

    @staticmethod
    def generate_node_dataclass(cls_: type["RuleChain"]):  # noqa: ANN205
        return dataclasses.dataclass(
            type(cls_.__name__, (object,), dict(cls_.__dict__))
        )

    @classmethod
    async def compose(cls, update: UpdateNode):
        globalns = globals()
        if "check_rule" not in globalns:
            globalns.update(
                {
                    "check_rule": getattr(
                        importlib.import_module("mubble.bot.dispatch.process"),
                        "check_rule",
                    ),
                },
            )

        ctx = Context()
        for rule in cls.rules:
            if not await check_rule(update.api, rule, update, ctx):
                raise ComposeError(f"Rule {rule!r} failed!")

        try:
            return cls.dataclass(**ctx)
        except Exception as exc:
            raise ComposeError(f"Dataclass validation error: {exc}")

    @classmethod
    def as_node(cls) -> type[typing.Self]:
        return cls

    @classmethod
    def get_sub_nodes(cls) -> dict:
        return {"update": UpdateNode}

    @classmethod
    def is_generator(cls) -> typing.Literal[False]:
        return False


__all__ = ("RuleChain",)
