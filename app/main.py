from contextlib import asynccontextmanager

from typing import AsyncIterator
from fastapi import FastAPI

from app.core.db.session import engine
from app.models.base import Base

from app.api.routers.link import router as link_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
app.include_router(router=link_router)