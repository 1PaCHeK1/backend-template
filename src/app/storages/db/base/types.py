import datetime
import uuid
from typing import Annotated

from sqlalchemy import (
    UUID,
    String,
    Text,
)
from sqlalchemy.orm import mapped_column
from uuid_utils.compat import uuid7

from lib.time import utc_now, utc_today

uuid_pk = Annotated[
    uuid.UUID,
    mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        insert_default=uuid7,
    ),
]

str_16 = Annotated[str, mapped_column(String(16))]
str_32 = Annotated[str, mapped_column(String(32))]
str_64 = Annotated[str, mapped_column(String(64))]
str_128 = Annotated[str, mapped_column(String(128))]
str_256 = Annotated[str, mapped_column(String(256))]

text = Annotated[str, mapped_column(Text)]

created_datetime = Annotated[
    datetime.datetime,
    mapped_column(insert_default=utc_now),
]

created_date = Annotated[
    datetime.date,
    mapped_column(insert_default=utc_today),
]
