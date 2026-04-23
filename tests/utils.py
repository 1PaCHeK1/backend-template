import uuid
from datetime import datetime
from typing import cast

import pytest

from lib.settings import get_settings
from tests.settings import TestSettings


def casefold_for_platform(s: str) -> str:
    settings = get_settings(TestSettings)
    return s.casefold() if settings.use_casefold else s


def uuid4_str() -> str:
    return str(uuid.uuid4())


def approx[T](value: T) -> T:
    return cast("T", pytest.approx(value))


def datetime_z_format(datetime_: datetime) -> str:
    return datetime_.isoformat().replace("+00:00", "Z")
