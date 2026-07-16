import os
from typing import AsyncIterator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.db.session import get_db
from app.main import app
from app.models.base import Base

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(os.environ["DATABASE_URL"])
TestingSessionLocal = async_sessionmaker(bind=engine)

async def get_test_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = get_test_db

@pytest_asyncio.fixture
async def test_db():
    async with TestingSessionLocal() as session:
        yield session

@pytest_asyncio.fixture(autouse=True)
async def setup_db() -> AsyncIterator[None]:
    async with engine.begin() as conn: # type: ignore
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn: # type: ignore
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest_asyncio.fixture
async def test_link(client):
    """Создаёт тестовую ссылку для тестов, которым она нужна"""
    response = await client.post("/links", json={"original_url": "https://example.com"})
    return response.json()