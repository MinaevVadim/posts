from pydantic import BaseModel


class ImageSchema(BaseModel):
    image: str | None
    post_id: int


class ViewImageSchema(BaseModel):
    image: str
