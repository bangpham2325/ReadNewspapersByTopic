from enum import Enum


class Roles(Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    AUTHOR = "AUTHOR"

    @classmethod
    def choices(cls):
        return ((value.name, value.value) for value in cls)
