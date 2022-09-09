import pytest
from freezegun import freeze_time
from tgbot.handlers.contacts import command_list


@pytest.fixture
def command_list_update(telegram_message_update, mbot):
    telegram_message_update.message.text = '/list'
    telegram_message_update.message.entities = [{'type': 'bot_command', 'offset': 0, 'length': 5}]
    return telegram_message_update


@freeze_time('2022-08-01')
def test_command_list(mbot, command_list_update, contact):
    command_list(command_list_update, {})

    assert mbot.text == 'Choose a contact from the list below:'
    assert mbot.reply_markup.inline_keyboard[0][0].text == 'Jane [A]'
    assert mbot.reply_markup.inline_keyboard[0][0].callback_data == 'EDIT_CONTACT:1'
