from sqlalchemy import literal, select
from sqlalchemy.ext.asyncio import AsyncSession


async def test_db_connection(session: AsyncSession) -> None:
    value = 1

    result = await session.scalar(select(literal(value)))

    assert value == result
