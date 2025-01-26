from sqlalchemy.ext.asyncio import AsyncSession
from models.images import Image
from utils.repository import SQLAlchemyBaseRepository, BaseImageRepository


class SQLAlchemyImageRepository(SQLAlchemyBaseRepository[Image], BaseImageRepository):
    """Repository image when using SQLAlchemy"""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Image)
