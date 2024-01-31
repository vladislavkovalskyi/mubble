from mubble.api import ABCAPI
from mubble.option import Nothing, Option, Some
from mubble.types import Update, UpdateType

from .base import BaseCute


class UpdateCute(BaseCute[Update], Update, kw_only=True):
    api: ABCAPI

    @property
    def update_type(self) -> Option[UpdateType]:
        for name, update in self.to_dict(
            exclude_fields={"update_id"},
        ).items():
            if update is not None:
                return Some(UpdateType(name))
        return Nothing


__all__ = ("UpdateCute",)
