from pydantic import BaseModel


class MediaCreateSchema(BaseModel):
    idd: int
    file: str | bytes


class MediaSchema(BaseModel):
    link: str
