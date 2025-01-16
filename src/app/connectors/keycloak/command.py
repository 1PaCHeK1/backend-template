import time
import uuid
from dataclasses import dataclass

import jwt
from result import Ok, Result

from .dto import DecodedTokenDTO
from .service import KeycloakService
from .settings import KeycloakSettings


@dataclass
class Authenticator:
    _service: KeycloakService[DecodedTokenDTO]
    _settings: KeycloakSettings

    async def execute(
        self, token: str
    ) -> Result[
        DecodedTokenDTO,
        jwt.ExpiredSignatureError | jwt.DecodeError | jwt.InvalidAudienceError,
    ]:
        if self._settings.fake_authentication:
            return Ok(self.fake_token())
        return await self._service.decode_token(token)

    def fake_token(self) -> DecodedTokenDTO:
        current_timestamp = int(time.time())
        return DecodedTokenDTO(
            exp=current_timestamp + 1_000,
            iat=current_timestamp,
            jti=str(uuid.uuid4()),
            iss="https://kc.domain.site/realms/test",
            aud=[self._settings.client_id],
            sub=uuid.uuid4(),
            typ="Bearer",
            azp="backend-auth-test",
            session_state=str(uuid.uuid4()),
            acr="0",
            scope="backend",
            sid=str(uuid.uuid4()),
        )
