import datetime


def utc_now() -> datetime.datetime:
    return datetime.datetime.now(tz=datetime.UTC)


def utc_now_without_ms() -> datetime.datetime:
    return datetime.datetime.now(tz=datetime.UTC).replace(microsecond=0)


def utc_today() -> datetime.date:
    return utc_now().date()
