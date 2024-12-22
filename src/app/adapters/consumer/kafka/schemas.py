from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class TestSchema(BaseModel):
    id: Annotated[UUID, Field(alias="guid")]
    name: str
    age: Annotated[int, Field(ge=1, le=200, description="Возраст")]
