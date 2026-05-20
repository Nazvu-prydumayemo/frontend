from tuiapp.api.client import APIClient
from tuiapp.api.court.schema import (
    Court,
    CourtResult,
    CourtsAll,
    CourtsAllResult,
    CourtSchedule,
    CourtScheduleResult,
)
from tuiapp.api.errors import APIError


class CourtService:
    def __init__(self, client: APIClient) -> None:
        self._client = client

    async def get_court(self, id: int) -> CourtResult:
        try:
            response = await self._client.get(f"/courts/{id}", response_model=Court)
            return CourtResult(message=f"Loaded court: {id}", status="success", court=response)

        except APIError as error:
            if error.status_code == 401:
                return CourtResult(message="Not authenticated", status="invalid", court=None)

            if error.status_code == 404:
                return CourtResult(message=f"Court {id} does not exist", status="error", court=None)

            if error.status_code == 422:
                return CourtResult(message="Invalid data provided", status="error", court=None)

            return CourtResult(
                message=f"Server Error: {error.status_code}", status="error", court=None
            )

    async def get_court_schedule(self, id: int) -> CourtScheduleResult:
        try:
            response = await self._client.get(
                f"/courts/{id}/schedule", response_model=list[CourtSchedule]
            )
            return CourtScheduleResult(
                message=f"Loaded schedule for court: {id}", status="success", schedule=response
            )

        except APIError as error:
            if error.status_code == 401:
                return CourtScheduleResult(
                    message="Not authenticated", status="invalid", schedule=None
                )

            if error.status_code == 404:
                return CourtScheduleResult(
                    message=f"Court {id} does not exist", status="error", schedule=None
                )

            if error.status_code == 422:
                return CourtScheduleResult(
                    message="Invalid data provided", status="error", schedule=None
                )

            return CourtScheduleResult(
                message=f"Server Error: {error.status_code}", status="error", schedule=None
            )

    async def get_all_courts(self, skip: int, limit: int = 10) -> CourtsAllResult:
        try:
            response = await self._client.get(
                f"/courts/?skip={skip}&limit={limit}", response_model=CourtsAll
            )
            return CourtsAllResult(message="Loaded all courts", status="success", courts=response)

        except APIError as error:
            if error.status_code == 401:
                return CourtsAllResult(message="Not authenticated", status="invalid", courts=None)

            return CourtsAllResult(
                message=f"Server Error: {error.status_code}", status="error", courts=None
            )
