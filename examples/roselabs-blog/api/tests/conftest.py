import os

import pytest
import sqlalchemy as sa
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool
from testcontainers.postgres import PostgresContainer

from alembic import command

# Ryuk (the reaper) flakes on port-mapping under Docker Desktop; the container's
# `with` context manager stops it on exit, so the reaper isn't needed.
os.environ.setdefault("TESTCONTAINERS_RYUK_DISABLED", "true")

_TRUNCATE = sa.text(
    "DO $$ DECLARE r RECORD; BEGIN "
    "FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname='public' "
    "AND tablename <> 'alembic_version') LOOP "
    "EXECUTE 'TRUNCATE TABLE ' || quote_ident(r.tablename) || ' CASCADE'; "
    "END LOOP; END $$;"
)


@pytest.fixture(scope="session")
def _pg():
    with PostgresContainer("postgres:16-alpine", driver="psycopg") as pg:
        yield pg


@pytest.fixture(scope="session")
def sync_url(_pg) -> str:
    return _pg.get_connection_url()


@pytest.fixture(scope="session")
def async_url(sync_url) -> str:
    return sync_url.replace("+psycopg", "+asyncpg")


@pytest.fixture(scope="session")
def migrated(sync_url, async_url) -> str:
    cfg = Config()
    cfg.set_main_option("script_location", "alembic")
    cfg.set_main_option("sqlalchemy.url", sync_url)
    command.upgrade(cfg, "head")
    return async_url


@pytest.fixture(scope="session")
def engine(migrated):
    return create_async_engine(migrated, poolclass=NullPool)


@pytest.fixture(autouse=True)
async def _clean(engine):
    yield
    async with engine.begin() as conn:
        await conn.execute(_TRUNCATE)


@pytest.fixture
async def session(engine):
    async with engine.connect() as conn:
        trans = await conn.begin()
        maker = async_sessionmaker(bind=conn, expire_on_commit=False)
        async with maker() as s:
            yield s
        await trans.rollback()


@pytest.fixture
async def db(engine):
    maker = async_sessionmaker(engine, expire_on_commit=False)
    async with maker() as s:
        yield s


@pytest.fixture
async def client(engine):
    maker = async_sessionmaker(engine, expire_on_commit=False)

    async def _override():
        async with maker() as s:
            yield s

    from app.core.db import get_session
    from app.main import app

    app.dependency_overrides[get_session] = _override
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.pop(get_session, None)
