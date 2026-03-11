from typing import Any, Self, TypeVar

import httpx
from pydantic import BaseModel
from pydantic.networks import AnyHttpUrl

from tuiapp.api.errors import APIError

T = TypeVar("T", bound=BaseModel)


class APIClient:
    """Client used to communicate with the Backend API."""

    def __init__(self, base_url: AnyHttpUrl, token: str | None = None) -> None:
        self._client = httpx.AsyncClient(
            base_url=str(base_url),
            headers={"Authorization": f"Bearer {token}"} if token else {},
            timeout=httpx.Timeout(10.0),
        )

    async def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        """Send an HTTP request to the API.

        Args:
            method: The HTTP method (GET, POST, etc.).
            endpoint: The API endpoint to request.
            **kwargs: Additional arguments to pass to the request.

        Returns:
            The JSON response from the API.

        Raises:
            APIError: If the request fails or returns an error status code.
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
        """Send an HTTP GET request to the API.

        Args:
            endpoint: The API endpoint to request.
            response_model: The Pydantic model to validate the response.
            **kwargs: Additional arguments to pass to the request.

        Returns:
            The validated response data as the specified model.
        """
        data = await self._request("GET", endpoint, **kwargs)
        return response_model.model_validate(data)

    async def post(self, endpoint: str, json: BaseModel, response_model: type[T], **kwargs) -> T:
        """Send an HTTP POST request to the API.

        Args:
            endpoint: The API endpoint to request.
            json: The data to send in the request body.
            response_model: The Pydantic model to validate the response.
            **kwargs: Additional arguments to pass to the request.

        Returns:
            The validated response data as the specified model.
        """
        data = await self._request("POST", endpoint, json=json, **kwargs)
        return response_model.model_validate(data)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self._client.aclose()
