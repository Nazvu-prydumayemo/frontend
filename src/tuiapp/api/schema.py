from typing import Literal

from pydantic import BaseModel


class Result(BaseModel):
    message: str
    status: Literal["success", "invalid", "error"]
