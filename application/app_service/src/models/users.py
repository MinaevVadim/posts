from typing import List, TYPE_CHECKING

from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db_config import Base


if TYPE_CHECKING:
    from models.posts import Post
    from models.comments import Comment


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    password: Mapped[bytes] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    following = relationship(
        "User",
        lambda: user_following,
        lazy="selectin",
        primaryjoin=lambda: User.id == user_following.c.user_id,
        secondaryjoin=lambda: User.id == user_following.c.following_id,
        backref="followers",
    )
    posts: Mapped[List["Post"]] = relationship()
    comments: Mapped[List["Comment"]] = relationship()


user_following = Table(
    "user_following",
    Base.metadata,
    Column("user_id", Integer, ForeignKey(User.id), primary_key=True),
    Column("following_id", Integer, ForeignKey(User.id), primary_key=True),
)
