from contextlib import asynccontextmanager
from uuid import uuid4

from typing import AsyncIterator
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost:5432/shortener"

engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(bind=engine)

async def get_db():
    async with SessionLocal() as session:
        yield session

class Base(DeclarativeBase):
    pass

class LinkORM(Base):
    __tablename__ = "links"
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    original_url: Mapped[str]
    short_code: Mapped[str]

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

class LinkSchema(BaseModel):
    id: str
    original_url: str
    short_code: str

def link_orm_to_model(link: LinkORM) -> LinkSchema:
    return LinkSchema(id=link.id, original_url=link.original_url, short_code=link.short_code)

app = FastAPI(lifespan=lifespan)

@app.get("/links")
async def read_links(db: AsyncSession = Depends(get_db)) -> list[LinkSchema]:
    result = await db.execute(select(LinkORM))
    links = result.scalars().all()
    return [link_orm_to_model(link) for link in links]
