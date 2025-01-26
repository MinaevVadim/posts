from typing import Sequence, AsyncGenerator

from log_config import logged, add_logger
from models.comments import Comment
from schemas.comments import CommentCreateSchema
from unit_of_work.utils import CommentUnitOfWork
from utils.specification import Specification


logger = add_logger(__name__)


@logged(logger)
class CommentService:
    """A class that allows you to work with comments"""

    def __init__(self, session: AsyncGenerator) -> None:
        self.session = session

    async def create_comment(self, comment: CommentCreateSchema) -> int:
        """Comment creation method"""
        comment_dict = comment.model_dump()
        async with CommentUnitOfWork(session_factory=self.session) as uow:
            comment_id = await uow.comments.add(comment_dict)
            await uow.commit()
            return comment_id

    async def get_comments(
        self, specification: Specification, idd: int
    ) -> Sequence[Comment]:
        """Method of receiving comments"""
        async with CommentUnitOfWork(session_factory=self.session) as uow:
            comments = await uow.comments.get_comments(specification, idd)
            return comments

    async def change_comment(
        self, idd: int, post: CommentCreateSchema
    ) -> Comment | None:
        """The method of changing the comment"""
        post_dict = post.model_dump(exclude_none=True)
        async with CommentUnitOfWork(session_factory=self.session) as uow:
            result = await uow.comments.update(idd, post_dict)
            await uow.commit()
            return result

    async def delete_comment(self, idd: int) -> bool | None:
        """Method of deleting a comment"""
        async with CommentUnitOfWork(session_factory=self.session) as uow:
            result = await uow.comments.delete(idd)
            await uow.commit()
            return result
