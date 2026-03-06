from typing import Any, Self, TypeVar

import httpx
from pydantic import BaseModel
from pydantic.networks import AnyHttpUrl

from tuiapp.api.errors import APIError

T = TypeVar("T", bound=BaseModel)


class APIClient:
    """
    - Client used to communicate with the API
    """

    def __init__(self, base_url: AnyHttpUrl, token: str | None = None) -> None:
        self._client = httpx.AsyncClient(
            base_url=str(base_url),
            headers={"Authorization": f"Bearer {token}"} if token else {},
            timeout=httpx.Timeout(10.0),
        )

    async def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        """
        - Private method for handling requests
        """

        try:
            response = await self._client.request(method, endpoint, **kwargs)
            response.raise_for_status()

            return response.json()

        except httpx.HTTPStatusError as error:
            raise APIError(error.response.status_code, str(error)) from error
        except httpx.RequestError as error:
            raise APIError(0, f"Request failed: {error}") from error

    async def get(self, endpoint: str, response_model: type[T], **kwargs) -> T:
        """
        - HTTP Get Request
        """

        data = await self._request("GET", endpoint, **kwargs)
        return response_model.model_validate(data)

    async def post(self, endpoint: str, json: BaseModel, response_model: type[T], **kwargs) -> T:
        """
        - HTTP Post Request
        """
        data = await self._request("POST", endpoint, json=json, **kwargs)
        return response_model.model_validate(data)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self._client.aclose()
