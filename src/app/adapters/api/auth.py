from http import HTTPStatus
from typing import Annotated

from aioinject import Inject
from aioinject.ext.fastapi import inject
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from result import Ok

from app.connectors.keycloak.command import Authenticator
from app.connectors.keycloak.dto import DecodedTokenDTO

_auth_scheme = APIKeyHeader(name="Authorization", auto_error=False)
AuthToken = Annotated[str | None, Depends(_auth_scheme)]

_unauthorized_exc = HTTPException(status_code=HTTPStatus.UNAUTHORIZED)


class JWTAuthenticator:
    def __init__(
        self,
        token: AuthToken,
        command: Authenticator,
    ) -> None:
        self._command = command
        self._token = token.removeprefix("Bearer ") if token else None

    async def authenticate(self) -> DecodedTokenDTO:
        _unauthorized_exc.headers = {"WWW-Authenticate": "Bearer"}

        if not self._token:
            raise _unauthorized_exc

        result = await self._command.execute(token=self._token)
        if isinstance(result, Ok):
            return result.ok_value

        raise _unauthorized_exc from result.err_value


@inject
async def _get_decoded_jwt(
    token: AuthToken,
    command: Annotated[Authenticator, Inject],
) -> DecodedTokenDTO:
    authenticator = JWTAuthenticator(token=token, command=command)
    return await authenticator.authenticate()


DecodedUserToken = Annotated[DecodedTokenDTO, Depends(_get_decoded_jwt)]
