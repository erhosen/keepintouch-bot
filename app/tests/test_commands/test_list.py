import pytest
from freezegun import freeze_time
from tgbot.handlers.contacts import command_list_old


@pytest.fixture
def command_list_update(telegram_message_update, mbot):
    telegram_message_update.message.text = '/list'
    telegram_message_update.message.entities = [{'type': 'bot_command', 'offset': 0, 'length': 5}]
    return telegram_message_update


@freeze_time('2022-08-01')
def test_command_list(mbot, command_list_update, contact):
    command_list_old(command_list_update, {})

    assert mbot.text == (
        'Here are your contacts:\n\n'
        '*List A:*\n'
        '[Jane](https://t.me/+78888888888) | a moment\n\n'
        '*List B:*\n\n'
        '*List C:*\n\n'
        '*List D:*\n\n'
    )
