from uuid import uuid4

from sqlalchemy.orm import mapped_column, Mapped

from app.models.base import Base

class LinkORM(Base):
    __tablename__ = "links"
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    original_url: Mapped[str]
    short_code: Mapped[str]
