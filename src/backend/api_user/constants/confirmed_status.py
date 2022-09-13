from enum import Enum


class Roles(Enum):
    ADMIN = "ADMIN"
    USER = "USER"

    @classmethod
    def choices(cls):
        return ((i.name, i.value) for i in cls)
