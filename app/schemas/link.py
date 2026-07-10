from pydantic import BaseModel, HttpUrl


class LinkSchema(BaseModel):
    id: str
    original_url: str
    short_code: str
    short_url: str

class LinkCreateSchema(BaseModel):
    original_url: HttpUrl