import secrets
import string

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import settings
from app.repository.link import LinkRepository
from app.schemas.link import LinkSchema, LinkCreateSchema


class LinkService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.link_repo = LinkRepository(db)

    async def list_links(self) -> list[LinkSchema]:
        links = await self.link_repo.get_all()
        return list(LinkSchema(
            id=link.id,
            original_url=link.original_url,
            short_code=link.short_code,
            short_url=f"{settings.BASE_URL}/{link.short_code}"
            ) for link in links)

    async def link_by_short_code(self, short_code: str) -> LinkSchema:
        link = await self.link_repo.get_by_short_code(short_code)
        return LinkSchema(
            id=link.id,
            original_url=link.original_url,
            short_code=link.short_code,
            short_url=f"{settings.BASE_URL}/{link.short_code}"
            )

    async def generate_unique_short_code(self, length=6) -> str:
        alphabet = string.ascii_letters + string.digits
        while True:
            code = ''.join(secrets.choice(alphabet) for _ in range(length))
            existing = await self.link_repo.exist_by_short_code(code)
            if not existing:
                return code

    async def create_link(self, link_create: LinkCreateSchema) -> LinkSchema:
        short_code = await self.generate_unique_short_code()
        link = await self.link_repo.create(link_create.original_url, short_code)
        await self.db.commit()
        await self.db.refresh(link)
        return LinkSchema(
            id=link.id,
            original_url=link.original_url,
            short_code=link.short_code,
            short_url=f"{settings.BASE_URL}/{link.short_code}"
            )


