from types import TracebackType
from typing import TYPE_CHECKING, Any

from faststream.broker.middlewares import BaseMiddleware

from app.di import create_container

if TYPE_CHECKING:
    from aioinject import InjectionContext


class AioinjectMiddleware(BaseMiddleware):
    def __init__(self, msg: Any = None) -> None:  # noqa: ANN401
        self.msg = msg
        self.context: InjectionContext | None = None

    async def on_receive(self) -> None:
        container = create_container()
        self.context = container.context()
        await self.context.__aenter__()

        return await super().on_receive()

    async def after_processed(
        self,
        exc_type: type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None,
    ) -> bool | None:
        if self.context:
            await self.context.__aexit__(
                exc_type=exc_type,
                exc_val=exc_val,
                exc_tb=exc_tb,
            )

        return await super().after_processed(
            exc_type=exc_type,
            exc_val=exc_val,
            exc_tb=exc_tb,
        )
