import pytest
from tgbot.core import Group
from tgbot.handlers import callback_set_group


@pytest.mark.parametrize('group', [Group.A, Group.B, Group.C, Group.D])
def test_callback_set_group(mbot, telegram_callback_update, contact, group):
    telegram_callback_update.callback_query.data = f'SET_GROUP:1:{group}'
    callback_set_group(telegram_callback_update, {})

    assert mbot.text == f"Jane is now in {group} list"
    contact.refresh_from_db()
    assert contact.group == group
