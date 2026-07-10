from pydantic import HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.link import LinkORM


class LinkRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all(self) -> list[LinkORM]:
        result = await self.db.execute(select(LinkORM))
        links = result.scalars().all()
        return list(links)

    async def get_by_short_code(self, short_code: str) -> LinkORM:
        result = await self.db.execute(
            select(LinkORM).where(LinkORM.short_code == short_code)
        )
        link = result.scalar_one_or_none()
        return link

    async def exist_by_short_code(self, short_code: str) -> bool:
        existing = await self.db.execute(
            select(LinkORM).where(LinkORM.short_code == short_code)
        )
        if not existing.scalar_one_or_none():
            return False
        return True

    async def create(self, original_url: HttpUrl, short_code: str) -> LinkORM:
        link = LinkORM(original_url=str(original_url), short_code=short_code)
        self.db.add(link)
        return link
