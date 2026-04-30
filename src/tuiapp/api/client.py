"""API client for communicating with the backend HTTP API."""

from collections.abc import Awaitable, Callable
from typing import Any, Self, TypeVar

import httpx
from pydantic import BaseModel, TypeAdapter
from pydantic.networks import AnyHttpUrl

from tuiapp.api.errors import APIError

T = TypeVar("T")


class APIClient:
    """Async HTTP client for communicating with the Backend API.

    Provides methods for making authenticated GET and POST requests with
    automatic token refresh on 401 responses.

    Attributes:
        _client: The underlying httpx AsyncClient instance.
        _on_401: Callback function to invoke on 401 responses.
    """

    def __init__(self, base_url: AnyHttpUrl) -> None:
        """Initialize the APIClient.

        Args:
            base_url: The base URL of the API backend.
        """
        self._client = httpx.AsyncClient(
            base_url=str(base_url),
            headers={},
            timeout=httpx.Timeout(10.0),
        )
        self._on_401: Callable[[], Awaitable[bool]] | None = None

    def set_access_token(self, token: str | None) -> None:
        """Update the Authorization header with the access token.

        Args:
            token: The access token to use, or None to remove the header.
        """
        if token:
            self._client.headers["Authorization"] = f"Bearer {token}"
        else:
            self._client.headers.pop("Authorization", None)

    def set_on_401_callback(self, on_401: Callable[[], Awaitable[bool]] | None = None) -> None:
        """Set a callback to handle 401 Unauthorized responses.

        The callback should attempt to refresh the access token and return
        True if successful (allowing a retry), or False to propagate the error.

        Args:
            on_401: Async callback function to invoke on 401 responses.
        """
        self._on_401 = on_401

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
        if "json" in kwargs and isinstance(kwargs["json"], BaseModel):
            kwargs["json"] = kwargs["json"].model_dump()

        try:
            response = await self._client.request(method, endpoint, **kwargs)
            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as error:
            if (
                error.response.status_code == 401
                and (
                    endpoint
                    not in {
                        "/auth/login",
                        "/auth/refresh",
                        "/auth/verify-reset-code",
                        "/auth/reset-password",
                    }
                )
                and self._on_401
            ):
                if await self._on_401():
                    try:
                        response = await self._client.request(method, endpoint, **kwargs)
                        response.raise_for_status()
                        return response.json()

                    except httpx.HTTPStatusError as retry_error:
                        raise APIError(
                            retry_error.response.status_code, str(retry_error)
                        ) from retry_error

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
        return TypeAdapter(response_model).validate_python(data)

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
        return TypeAdapter(response_model).validate_python(data)

    async def patch(self, endpoint: str, json: BaseModel, response_model: type[T], **kwargs) -> T:
        """Send an HTTP PATCH request to the API.

        Args:
            endpoint: The API endpoint to request.
            json: The data to send in the request body.
            response_model: The Pydantic model to validate the response.
            **kwargs: Additional arguments to pass to the request.

        Returns:
            The validated response data as the specified model.
        """
        data = await self._request("PATCH", endpoint, json=json, **kwargs)
        return TypeAdapter(response_model).validate_python(data)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self._client.aclose()
