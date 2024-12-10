import abc
import typing

from mubble.tools.adapter.event import EventAdapter
from mubble.types.objects import Message as MessageEvent

from .abc import ABCRule, CheckResult, Message


class MessageRule(
    ABCRule[Message], abc.ABC, adapter=EventAdapter(MessageEvent, Message)
):
    @abc.abstractmethod
    def check(self, *args: typing.Any, **kwargs: typing.Any) -> CheckResult: ...


__all__ = ("MessageRule",)
