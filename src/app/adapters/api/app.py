import contextlib
from collections.abc import AsyncGenerator, Iterable

from aioinject.ext.fastapi import AioInjectMiddleware
from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.adapters.api import v1
from app.adapters.api.settings import ApiSettings
from app.di import create_container
from app.telemetry import setup_telemetry
from app.version import __version__
from lib.settings import get_settings

_routers: Iterable[APIRouter] = [
    v1.router,
]


@contextlib.asynccontextmanager
async def _lifespan(_: FastAPI) -> AsyncGenerator[None]:
    async with create_container():
        yield


def create_app() -> FastAPI:
    setup_telemetry(source="api")

    settings = get_settings(ApiSettings)
    app = FastAPI(
        lifespan=_lifespan,
        title="Title",
        description="Description",
        version=__version__,
    )

    for router in _routers:
        app.include_router(router)

    app.add_middleware(AioInjectMiddleware, container=create_container())
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=settings.cors_allow_origins,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )

    @app.get("/health")
    async def health_check() -> None:  # pyright: ignore[reportUnusedFunction]
        return None

    return app
