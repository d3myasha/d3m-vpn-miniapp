"""Инициализация базы данных."""

from app.db.base import Base, engine


async def init_db() -> None:
    """Инициализация базы данных - создание таблиц."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db() -> None:
    """Удаление всех таблиц базы данных."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
