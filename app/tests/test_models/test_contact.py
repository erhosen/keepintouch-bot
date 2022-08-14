import pytest
from tgbot.core import Group


@pytest.mark.parametrize('group, demoted', [(Group.A, Group.B), (Group.B, Group.C), (Group.C, Group.D)])
def test_demote(contact, group, demoted):
    contact.group = group
    contact.save()

    contact.demote()

    contact.refresh_from_db()
    assert contact.group == demoted


def test_demote_final(contact):
    contact.group = Group.D
    contact.save()

    with pytest.raises(ValueError):
        contact.demote()

    contact.refresh_from_db()
    assert contact.group == Group.D
