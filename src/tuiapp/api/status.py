from datetime import datetime

from pydantic import BaseModel

from tuiapp.api.client import APIClient


class StatusResponse(BaseModel):
    """Response model for the API status endpoint.

    Attributes:
        status: The current status of the API (e.g., "ok", "error").
        timestamp: The timestamp when the status was checked.
    """

    status: str
    timestamp: datetime


class StatusCheckService:
    """Service for checking the API status."""

    def __init__(self, client: APIClient) -> None:
        """Initialize the status service.

        Args:
            client: The API client for making requests.
        """
        self._client = client

    async def check_status(self) -> StatusResponse:
        """Check the current status of the API.

        Returns:
            The status response containing the API status and timestamp.
        """
        return await self._client.get("/status/", response_model=StatusResponse)

    async def status_summary(self) -> str:
        """Get a human-readable summary of the API status.

        Returns:
            A formatted string with the status and timestamp.
        """
        status = await self.check_status()
        return f"{status.status}, {status.timestamp}"
