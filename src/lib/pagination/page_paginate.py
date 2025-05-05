from collections.abc import AsyncIterator, Awaitable, Callable
from typing import Concatenate

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from lib.pagination.dto import (
    PagePaginationInfoDTO,
    PagePaginationParamsDTO,
    PagePaginationResultDTO,
)


async def paginate_statement[TModel: DeclarativeBase](
    *,
    session: AsyncSession,
    statement: Select[tuple[TModel]],
    pagination: PagePaginationParamsDTO,
    count_query: Select[tuple[int]] | None = None,
) -> PagePaginationResultDTO[TModel]:
    items_query = statement.limit(pagination.page_size).offset(
        (pagination.page - 1) * pagination.page_size,
    )
    items = (await session.scalars(items_query)).all()

    if count_query is None:
        count_query = select(func.count()).select_from(
            statement.order_by(None).subquery()
        )
    total_items = (await session.execute(count_query)).scalar_one()

    page_info = PagePaginationInfoDTO(
        current_page=pagination.page,
        page_size=pagination.page_size,
        total_items=total_items,
        has_next_page=pagination.page * pagination.page_size < total_items,
        has_previous_page=pagination.page > 1,
    )
    return PagePaginationResultDTO(
        items=items,
        page_info=page_info,
    )


async def paginate_endpoint[**P, T](
    endpoint: Callable[
        Concatenate[PagePaginationParamsDTO, P],
        Awaitable[PagePaginationResultDTO[T]],
    ],
    pagination_params: PagePaginationParamsDTO,
    *args: P.args,
    **kwargs: P.kwargs,
) -> AsyncIterator[T]:
    result = await endpoint(pagination_params, *args, **kwargs)
    for i in result.items:
        yield i

    while result.page_info.has_next_page:
        pagination_params.page += 1
        result = await endpoint(pagination_params, *args, **kwargs)
        for i in result.items:
            yield i
