import pytest
from app.services.link import LinkService
from app.schemas.link import LinkCreateSchema

@pytest.mark.asyncio
async def test_generate_unique_short_code(test_db):
    service = LinkService(test_db)
    code1 = await service.generate_unique_short_code()
    code2 = await service.generate_unique_short_code()

    assert len(code1) == 6
    assert len(code2) == 6
    assert code1 != code2