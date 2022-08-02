from enum import Enum


class Group(str, Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'

    @classmethod
    def choices(self):
        return [(choice.name, choice.value) for choice in self]


GROUP_POLICY = {
    Group.A: 21,
    Group.B: 60,
    Group.C: 180,
    Group.D: 365,
}


class KeepintouchNotifyChoices(str, Enum):
    DONE = 'done'
    DEMOTE = 'demote'
    DELETE = 'delete'
