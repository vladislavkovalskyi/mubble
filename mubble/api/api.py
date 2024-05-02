import typing

import msgspec
from fntypes.result import Error, Ok, Result

from mubble.api.response import APIResponse
from mubble.client import ABCClient, AiohttpClient
from mubble.model import DataConverter, decoder
from mubble.types.methods import APIMethods

from .abc import ABCAPI, APIError, Token


def compose_data(
    client: ABCClient,
    data: dict[str, typing.Any],
    files: dict[str, tuple[str, bytes]],
) -> typing.Any:
    converter = DataConverter(files=files.copy())
    return client.get_form(
        data={k: converter(v) for k, v in data.items()},
        files=converter.files,
    )


class API(ABCAPI, APIMethods):
    """Bot API with available API methods."""

    API_URL = "https://api.telegram.org/"

    def __init__(self, token: Token, *, http: ABCClient | None = None) -> None:
        self.token = token
        self.http = http or AiohttpClient()
        super().__init__(self)
    
    def __repr__(self) -> str:
        return "<{}: token={!r}, http={!r}>".format(
            self.__class__.__name__,
            self.token,
            self.http,
        )

    @property
    def id(self) -> int:
        return self.token.bot_id

    @property
    def request_url(self) -> str:
        return self.API_URL + f"bot{self.token}/"

    async def request(
        self,
        method: str,
        data: dict[str, typing.Any] | None = None,
        files: dict[str, tuple[str, bytes]] | None = None,
    ) -> Result[dict[str, typing.Any] | list[typing.Any] | bool, APIError]:
        response = await self.http.request_json(
            url=self.request_url + method,
            data=compose_data(self.http, data or {}, files or {})
        )
        if response.get("ok"):
            assert "result" in response
            return Ok(response["result"])
        return Error(APIError(
            code=response.get("error_code", 400),
            error=response.get("description"),
        ))

    async def request_raw(
        self,
        method: str,
        data: dict[str, typing.Any] | None = None,
        files: dict[str, tuple[str, bytes]] | None = None,
    ) -> Result[msgspec.Raw, APIError]:
        response_bytes = await self.http.request_bytes(
            url=self.request_url + method,
            data=compose_data(self.http, data or {}, files or {}),
        )
        return decoder.decode(response_bytes, type=APIResponse).to_result()


__all__ = ("API",)
