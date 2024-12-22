from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DecodedTokenDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        frozen=True,
    )

    exp: int
    iat: int
    jti: str
    iss: str
    aud: list[str]
    sub: UUID
    typ: str
    azp: str
    session_state: str
    acr: str
    realm_access: dict[str, list[str] | dict[str, list[str]]]
    resource_access: dict[str, list[str] | dict[str, list[str]]]
    scope: str
    sid: str
