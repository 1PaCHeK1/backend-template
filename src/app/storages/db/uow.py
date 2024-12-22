from collections.abc import Iterable

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


class UnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def add(self, obj: DeclarativeBase) -> None:
        self._session.add(obj)

    def add_all(self, objs: Iterable[DeclarativeBase]) -> None:
        self._session.add_all(objs)

    async def save_changes(self) -> None:
        await self._session.flush()
