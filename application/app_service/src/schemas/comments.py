from datetime import datetime

from pydantic import BaseModel, ConfigDict

from utils.common import TypeComment


class CommentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date: datetime
    karma: int
    content: str
    approved: bool
    type: TypeComment
    author_id: int
    post_id: int


class CommentCreateSchema(BaseModel):
    karma: int
    content: str
    type: TypeComment = None
    author_id: int
    post_id: int


class CommentUpdateSchema(BaseModel):
    karma: int = None
    content: str = None
    type: TypeComment = None


class CommentIDSchema(BaseModel):
    comment_id: int


class ResultCommentSchema(BaseModel):
    result: bool
