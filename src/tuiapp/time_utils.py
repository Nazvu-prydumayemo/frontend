"""Time zone conversion utilities."""

from datetime import UTC, date, datetime, time


def utc_to_local(t: time) -> time:
    """Convert a UTC time to the local time zone.

    Args:
        t: A time object in UTC.

    Returns:
        The equivalent time in the local time zone.
    """
    dt = datetime.combine(date.today(), t, tzinfo=UTC)
    return dt.astimezone().time()


def local_to_utc(t: time) -> time:
    """Convert a local time to UTC.

    Args:
        t: A time object in the local time zone.

    Returns:
        The equivalent time in UTC.
    """
    local_tz = datetime.now().astimezone().tzinfo
    dt = datetime.combine(date.today(), t, tzinfo=local_tz)
    return dt.astimezone(UTC).time()
