from enum import Enum

from dateutil.relativedelta import relativedelta


class Group(str, Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'

    @classmethod
    def choices(self):
        return [(choice.name, choice.value) for choice in self]


GROUP_POLICY = {
    Group.A: relativedelta(weeks=3),
    Group.B: relativedelta(months=2),
    Group.C: relativedelta(months=6),
    Group.D: relativedelta(years=1),
}


class KeepintouchNotifyChoices(str, Enum):
    DONE = 'done'
    DEMOTE = 'demote'
    DELETE = 'delete'
