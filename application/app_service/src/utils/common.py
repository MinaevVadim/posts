import enum


class Status(enum.Enum):
    PUBLISHED = "published"
    FUTURE = "future"
    DRAFT = "draft"
    PENDING = "pending"
    PRIVATE = "private"
    TRASH = "trash"


class StatusComment(enum.Enum):
    OPEN = "open"
    PENDING = "pending"
    APPROVED = "approved"


class TypePost(enum.Enum):
    SELLER = "seller"
    INFORMATION = "information"
    ENGAGING = "engaging"
    ENTERTAINMENT = "entertainment"
    EDUCATIONAL = "educational"
    CUSTOM = "custom"


class TypeComment(enum.Enum):
    TEXTUAL = "textual"
    CONCEPTUAL = "conceptual"
