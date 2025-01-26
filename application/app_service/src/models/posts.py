from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, Mapper

from db.db_config import Base

from utils.common import Status, StatusComment, TypePost

if TYPE_CHECKING:
    from models.comments import Comment
    from models.images import Image


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now()
    )
    modified: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now()
    )
    name: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    excerpt: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[Status] = mapped_column(default=Status.PUBLISHED)
    status_comment: Mapped[StatusComment] = mapped_column(default=StatusComment.OPEN)
    type: Mapped[TypePost] = mapped_column(default=TypePost.ENTERTAINMENT)
    comment_count: Mapped[int] = mapped_column(default=0)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    comments: Mapped[List["Comment"]] = relationship()
    images: Mapped[List["Image"]] = relationship("Image", cascade="all,delete")

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "modified": self.modified,
            "name": self.name,
            "content": self.content,
            "excerpt": self.excerpt,
            "status": self.status,
            "status_comment": self.status_comment,
            "type": self.type,
            "comment_count": self.comment_count,
            "images": [i for i in self.images],
        }
