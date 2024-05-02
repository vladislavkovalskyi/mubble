import typing

from fntypes.co import Nothing, Some

from mubble.api import ABCAPI
from mubble.msgspec_utils import Option
from mubble.types import Model, Update

from .base import BaseCute

ModelT = typing.TypeVar("ModelT", bound=Model)


class UpdateCute(BaseCute[Update], Update, kw_only=True):
    api: ABCAPI

    @property
    def incoming_update(self) -> Model:
        return getattr(
            self,
            self.update_type.expect("Update object has no incoming update.").value,
        )
    
    def get_event(self, event_model: type[ModelT]) -> Option[ModelT]:
        if isinstance(self.incoming_update, event_model):
            return Some(self.incoming_update)
        return Nothing()


__all__ = ("UpdateCute",)
