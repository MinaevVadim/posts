from abc import ABC

from sqlalchemy import ColumnElement

from models.comments import Comment
from models.posts import Post
from utils.common import Status, TypeComment


class Specification(ABC):
    """
    An abstract class specification that describes the requirements
    for business objects and uses them for filtering
    """

    def is_satisfied(self) -> bool:
        raise NotImplementedError()


class IsStatusSpecification(Specification):
    """Class specification for filtering by status"""

    def __init__(self, status: Status) -> None:
        self.status = status

    def is_satisfied(self) -> ColumnElement[bool] | bool:
        if self.status:
            return Post.status == self.status
        return True


class IsTypeSpecification(Specification):
    """Class specification for filtering by type"""

    def __init__(self, type_name: TypeComment) -> None:
        self.type_name = type_name

    def is_satisfied(self) -> ColumnElement[bool] | bool:
        if self.type_name:
            return Comment.type == self.type_name
        return True
