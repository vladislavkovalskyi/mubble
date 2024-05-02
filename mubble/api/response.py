import msgspec
from fntypes.result import Error, Ok, Result

from mubble.api.error import APIError
from mubble.model import Model


class APIResponse(Model):
    ok: bool = False
    result: msgspec.Raw = msgspec.Raw(b"")
    error_code: int = 0
    description: str = ""

    def to_result(self) -> Result[msgspec.Raw, APIError]:
        if self.ok:
            return Ok(self.result)
        return Error(APIError(self.error_code, self.description))


__all__ = ("APIResponse",)
