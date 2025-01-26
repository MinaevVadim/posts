from typing import AsyncGenerator

from log_config import add_logger, logged
from schemas.images import ImageSchema
from unit_of_work.utils import ImageUnitOfWork

logger = add_logger(__name__)


@logged(logger)
class ImageService:
    """A class that allows you to work with images"""

    def __init__(self, session: AsyncGenerator) -> None:
        self.session = session

    async def create_image(self, data: ImageSchema) -> int:
        """Image creation method"""
        image_dict = data.model_dump()
        async with ImageUnitOfWork(session_factory=self.session) as uow:
            image_id = await uow.images.add(image_dict)
            await uow.commit()
            return image_id
