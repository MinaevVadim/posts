import json
from datetime import datetime

from pydantic import BaseModel, model_validator, ConfigDict

from schemas.images import ViewImageSchema
from utils.common import Status, StatusComment, TypePost


class PostSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date: datetime
    modified: datetime
    name: str
    content: str
    excerpt: str
    status: Status
    status_comment: StatusComment
    type: TypePost
    comment_count: int
    images: list[ViewImageSchema]


class PostCreateSchema(BaseModel):
    name: str
    content: str
    excerpt: str
    author_id: int

    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class PostUpdateSchema(BaseModel):
    name: str = None
    content: str = None
    excerpt: str = None
    status: Status = None
    status_comment: StatusComment = None
    author_id: int = None


class IDPostSchema(BaseModel):
    post_id: int


class ResultPostSchema(BaseModel):
    result: bool
