from contextlib import asynccontextmanager
from uuid import uuid4
import secrets, string

from typing import AsyncIterator
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, HttpUrl
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from starlette.responses import RedirectResponse

DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost:5432/postgres"

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
    short_url: str

class LinkCreate(BaseModel):
    original_url: HttpUrl

def link_orm_to_model(link: LinkORM) -> LinkSchema:
    return LinkSchema(id=link.id, original_url=link.original_url, short_code=link.short_code)

app = FastAPI(lifespan=lifespan)

async def generate_unique_short_code(db: AsyncSession, length=6) -> str:
    alphabet = string.ascii_letters + string.digits
    while True:
        code = ''.join(secrets.choice(alphabet) for _ in range(length))
        existing = await db.execute(select(LinkORM).where(LinkORM.short_code == code))
        if not existing.scalar_one_or_none():
            return code

@app.get("/links")
async def read_links(db: AsyncSession = Depends(get_db)) -> list[LinkSchema]:
    result = await db.execute(select(LinkORM))
    links = result.scalars().all()
    return [link_orm_to_model(link) for link in links]

@app.post("/links")
async def create_link(payload: LinkCreate, db: AsyncSession = Depends(get_db)) -> LinkSchema:
    short_code = await generate_unique_short_code(db)
    link = LinkORM(original_url=str(payload.original_url), short_code=short_code)
    db.add(link)
    await db.commit()
    await db.refresh(link)
    return LinkSchema(id=link.id, original_url=link.original_url,
                      short_code=short_code, short_url=f"http://localhost:8000/{link.short_code}")

@app.get("/{short_code}")
async def redirect_to_original(short_code: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(LinkORM).where(LinkORM.short_code == short_code))
    link = result.scalar_one_or_none()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return RedirectResponse(url=link.original_url)