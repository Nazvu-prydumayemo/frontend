from datetime import datetime

from pydantic import BaseModel

from tuiapp.api.client import APIClient


class StatusResponse(BaseModel):
    """
    - Response model for status checks
    """

    status: str
    timestamp: datetime


class StatusService:
    """
    - Used to get the status of the api
    """

    def __init__(self, client: APIClient) -> None:
        self._client = client

    async def check_status(self) -> StatusResponse:
        return await self._client.get("/status/", response_model=StatusResponse)

    async def status_summary(self) -> str:
        status = await self.check_status()
        return f"{status.status}, {status.timestamp}"
