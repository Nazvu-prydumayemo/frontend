"""Common Pydantic schemas shared across the API."""

from typing import Literal

from pydantic import BaseModel


class Result(BaseModel):
    """Base result model for API operations.

    A generic result wrapper used by various API services to return
    success or failure information.

    Attributes:
        message: A descriptive message about the result of the operation.
        status: The status of the operation indicating success or type of failure.
    """

    message: str
    status: Literal["success", "invalid", "error"]


class Message(BaseModel):
    message: str
