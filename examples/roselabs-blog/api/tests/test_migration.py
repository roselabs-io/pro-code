import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool


async def test_migration_creates_authors_table_from_empty(migrated: str) -> None:
    engine = create_async_engine(migrated, poolclass=NullPool)
    async with engine.connect() as conn:
        result = await conn.execute(sa.text("select to_regclass('public.authors')"))
        assert result.scalar() == "authors"
    await engine.dispose()
