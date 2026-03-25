import os
import functools
import typing

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)
from sqlalchemy.pool import NullPool

from core.config import settings


@functools.lru_cache
def get_engine(url: str | URL | None = None, **kwargs) -> AsyncEngine:
    poolclass = NullPool if os.environ.get("ENVIRONMENT") == "test" else None

    return create_async_engine(
        url or settings().postgres_dsn,
        echo=False,
        future=True,
        poolclass=poolclass,
        **kwargs,
    )


def get_async_sessionmaker(
    url: str | URL | None = None,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        get_engine(url or settings().postgres_dsn), expire_on_commit=False
    )


async def get_session() -> typing.AsyncGenerator[AsyncSession, None]:
    async_session = get_async_sessionmaker()
    async with async_session() as session:
        yield session
