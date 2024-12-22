from fastapi import APIRouter

from app.adapters.api.auth import DecodedUserToken
from app.adapters.api.v1.user.schemas import UserSimpleSchema

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get("/me")
async def user_me(token: DecodedUserToken) -> UserSimpleSchema:
    return UserSimpleSchema(
        id=token.sub,
    )
