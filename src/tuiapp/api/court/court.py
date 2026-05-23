"""Court service for managing court-related operations."""

from datetime import date

from tuiapp.api.client import APIClient
from tuiapp.api.court.schema import (
    Court,
    CourtResult,
    CourtsAll,
    CourtsAllResult,
    CourtSchedule,
    CourtScheduleResult,
    CourtScheduleSlotsAll,
    CourtScheduleSlotsAllResult,
)
from tuiapp.api.errors import APIError


class CourtService:
    """Service for managing court-related API operations.

    Provides methods for fetching court details, schedules, available slots,
    and listing all courts with pagination.

    Attributes:
        _client: The API client used for making requests.
    """

    def __init__(self, client: APIClient) -> None:
        """Initialize the CourtService.

        Args:
            client: The APIClient instance for making API requests.
        """
        self._client = client

    async def get_court(self, id: int) -> CourtResult:
        """Fetch details for a specific court by ID.

        Args:
            id: The unique identifier of the court.

        Returns:
            CourtResult containing the court data on success,
            or error status and message on failure.
        """
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
        """Fetch the weekly schedule for a specific court.

        Args:
            id: The unique identifier of the court.

        Returns:
            CourtScheduleResult containing the schedule on success,
            or error status and message on failure.
        """
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

    async def get_court_available_slots(self, id: int, date: date) -> CourtScheduleSlotsAllResult:
        """Fetch available booking slots for a court on a specific date.

        Args:
            id: The unique identifier of the court.
            date: The date to query for available slots.

        Returns:
            CourtScheduleSlotsAllResult containing available slots on success,
            or error status and message on failure.
        """
        try:
            response = await self._client.get(
                f"/courts/{id}/available-slots?slot_date={date.strftime('%Y-%m-%d')}",
                response_model=CourtScheduleSlotsAll,
            )
            return CourtScheduleSlotsAllResult(
                message=f"Loaded schedule for court: {id}", status="success", slots=response
            )

        except APIError as error:
            if error.status_code == 400:
                return CourtScheduleSlotsAllResult(
                    message=f"Can only query 7 days from {date}", status="invalid", slots=None
                )

            if error.status_code == 401:
                return CourtScheduleSlotsAllResult(
                    message="Not authenticated", status="invalid", slots=None
                )

            if error.status_code == 404:
                return CourtScheduleSlotsAllResult(
                    message=f"Court {id} does not exist", status="error", slots=None
                )

            if error.status_code == 422:
                return CourtScheduleSlotsAllResult(
                    message="Invalid data provided", status="error", slots=None
                )

            return CourtScheduleSlotsAllResult(
                message=f"Server Error: {error.status_code}", status="error", slots=None
            )

    async def get_all_courts(self, skip: int, limit: int = 10) -> CourtsAllResult:
        """Fetch a paginated list of all courts.

        Args:
            skip: The number of courts to skip (for pagination).
            limit: The maximum number of courts to return (default: 10).

        Returns:
            CourtsAllResult containing the list of courts on success,
            or error status and message on failure.
        """
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
