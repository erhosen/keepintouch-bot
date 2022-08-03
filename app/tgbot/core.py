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


class CallbackMarker(str, Enum):
    SET_GROUP = 'SET_GROUP'
    KEEPINTOUCH = "KEEPINTOUCH"


GROUP_POLICY = {
    Group.A: relativedelta(weeks=3),
    Group.B: relativedelta(months=2),
    Group.C: relativedelta(months=6),
    Group.D: relativedelta(years=1),
}


class KeepintouchChoices(str, Enum):
    OK = 0
    TOMORROW = 1
    IN_A_WEEK = 7
    DEMOTE = -1


KEEPINTOUCH_RULES = """
• *A list:* Very important people. Contact every three weeks.
• *B list:* Important people. Contact every two months.
• *C list:* Most people. Contact every six months.
• *D list:* Demoted people. Contact once a year, to make sure you still have their correct info.
"""

SHARE_CONTACT_TUTOR_IMG = 'https://www.wikihow.com/images/thumb/a/a1/Find-Contacts-on-Telegram-on-Android-Step-15.jpg/v4-460px-Find-Contacts-on-Telegram-on-Android-Step-15.jpg'  # noqa
