from enum import Enum


class StarRating(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

    @classmethod
    def choices(cls):
        return ((i.value, i.name) for i in cls)
