from datetime import UTC, date, datetime, time


def utc_to_local(t: time) -> time:
    dt = datetime.combine(date.today(), t, tzinfo=UTC)
    return dt.astimezone().time()


def local_to_utc(t: time) -> time:
    local_tz = datetime.now().astimezone().tzinfo
    dt = datetime.combine(date.today(), t, tzinfo=local_tz)
    return dt.astimezone(UTC).time()
