import pytest
from tgbot.core import SHARE_CONTACT_TUTOR_IMG
from tgbot.handlers import command_add_contact


@pytest.fixture
def add_contact_command_update(telegram_message_update, mbot):
    telegram_message_update.message.text = '/add_contact'
    telegram_message_update.message.entities = [{'type': 'bot_command', 'offset': 0, 'length': 13}]
    return telegram_message_update


def test_command_add_contact(mbot, add_contact_command_update):
    command_add_contact(add_contact_command_update, {})

    assert mbot.caption == 'Share your contact with me\n\nBTW, you can do it without /add_contact'
    assert mbot.photo == SHARE_CONTACT_TUTOR_IMG
