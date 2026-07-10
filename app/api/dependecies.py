from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db
from app.services.link import LinkService


def get_link_service(db: AsyncSession = Depends(get_db)) -> LinkService:
    """Функция для зависимости LinkService"""
    return LinkService(db)