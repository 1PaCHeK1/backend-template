from fastapi import APIRouter

from . import user

router = APIRouter(
    prefix="/v1",
    tags=["v1"],
)

router.include_router(user.router)
