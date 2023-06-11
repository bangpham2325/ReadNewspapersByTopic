from enum import Enum


class PostStatus(Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    PENDING = "PENDING"

    @classmethod
    def choices(cls):
        return ((i.name, i.value) for i in cls)
