from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.responses import RedirectResponse

from app.api.dependecies import get_link_service
from app.schemas.link import LinkSchema, LinkCreateSchema
from app.services.link import LinkService

router = APIRouter()

@router.get("/links")
async def read_links(link_service: LinkService = Depends(get_link_service)) -> list[LinkSchema]:
    return await link_service.list_links()

@router.post("/links", status_code=status.HTTP_201_CREATED)
async def create_link(payload: LinkCreateSchema, link_service: LinkService = Depends(get_link_service)) -> LinkSchema:
    return await link_service.create_link(link_create=payload)

@router.get("/{short_code}")
async def redirect_to_original(short_code: str, link_service: LinkService = Depends(get_link_service)):
    link = await link_service.link_by_short_code(short_code)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return RedirectResponse(url=link.original_url)