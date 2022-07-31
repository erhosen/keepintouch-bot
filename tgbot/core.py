from enum import Enum


class Group(str, Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'

    @classmethod
    def choices(self):
        return [(choice.name, choice.value) for choice in self]
