from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.db_config import Base


class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    image: Mapped[str]
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
