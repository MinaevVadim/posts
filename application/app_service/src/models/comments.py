from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from db.db_config import Base
from utils.common import TypeComment


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now()
    )
    karma: Mapped[int] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    approved: Mapped[bool] = mapped_column(
        server_default=expression.true(), default=True, nullable=False
    )
    type: Mapped[TypeComment] = mapped_column(default=TypeComment.TEXTUAL)
    comment_count: Mapped[int] = mapped_column(default=0)

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
