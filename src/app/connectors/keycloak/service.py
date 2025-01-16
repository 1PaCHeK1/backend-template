from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, cast

import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from keycloak import KeycloakOpenID
from pydantic import BaseModel
from result import Err, Ok, Result

if TYPE_CHECKING:
    from cryptography.hazmat.primitives.asymmetric.types import PublicKeyTypes


class KeycloakService[TKeycloakTokenDTO: BaseModel]:
    __token_dto__: type[TKeycloakTokenDTO]

    _grant_type = "authorization_code"
    _public_key_template = (
        "-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"
    )

    def __init__(  # noqa: PLR0913
        self,
        token_dto: type[TKeycloakTokenDTO],
        server_url: str,
        client_id: str,
        realm_name: str,
        client_secret_key: str,
        encoding_algorithm: str,
    ) -> None:
        self.__token_dto__ = token_dto
        self._kc_open_id = KeycloakOpenID(
            server_url=server_url,
            client_id=client_id,
            realm_name=realm_name,
            client_secret_key=client_secret_key,
        )
        self._encode_algorithm = encoding_algorithm
        self._cached_public_key: PublicKeyTypes | None = None
        self._public_key_lock = asyncio.Lock()

    async def get_public_key(self) -> PublicKeyTypes:
        if self._cached_public_key is None:
            async with self._public_key_lock:
                if self._cached_public_key is None:
                    public_key = self._public_key_template.format(
                        public_key=cast(str, await self._kc_open_id.public_key()),
                    )
                    self._cached_public_key = serialization.load_pem_public_key(
                        public_key.encode(),
                        backend=default_backend(),
                    )
        return self._cached_public_key

    async def decode_token(
        self,
        token: str,
    ) -> Result[
        TKeycloakTokenDTO,
        jwt.ExpiredSignatureError | jwt.DecodeError | jwt.InvalidAudienceError,
    ]:
        try:
            decoded_token = await self._decode_token(token=token)
            return Ok(value=decoded_token)
        except (
            jwt.ExpiredSignatureError,
            jwt.DecodeError,
            jwt.InvalidAudienceError,
        ) as e:
            return Err(e)

    async def verify_token(self, token: str) -> bool:
        decoded_token = await self.decode_token(token=token)
        return isinstance(decoded_token, Ok)

    async def _decode_token(self, token: str) -> TKeycloakTokenDTO:
        public_key = await self.get_public_key()
        decoded_token = jwt.decode(
            jwt=token,
            key=public_key,  # pyright: ignore[reportArgumentType]
            algorithms=[self._encode_algorithm],
            audience=cast(str, self._kc_open_id.client_id),
            options={
                "verify_aud": True,
                "verify_exp": True,
            },
        )
        return self.__token_dto__.model_validate(decoded_token)
