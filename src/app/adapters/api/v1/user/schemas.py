import uuid

from app.adapters.api.schemas import BaseSchema


class UserSimpleSchema(BaseSchema):
    id: uuid.UUID
