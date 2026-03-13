from datetime import datetime

from pydantic import BaseModel


class StatusResponse(BaseModel):
    """Response model for the API status endpoint.

    Attributes:
        status: The current status of the API (e.g., "ok", "error").
        timestamp: The timestamp when the status was checked.
    """

    status: str
    timestamp: datetime
