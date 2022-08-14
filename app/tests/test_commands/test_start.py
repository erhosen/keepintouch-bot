import pytest
from tgbot.handlers import command_start
from tgbot.models import User


@pytest.fixture
def start_command_update(telegram_message_update, mbot):
    telegram_message_update.message.text = '/start'
    telegram_message_update.message.entities = [{'type': 'bot_command', 'offset': 0, 'length': 6}]
    return telegram_message_update


def test_start_command_new_user(mbot, start_command_update):
    command_start(start_command_update, {})

    assert mbot.text == 'Sup, John!'
    assert User.objects.get(user_id=start_command_update.message.from_user.id).first_name == 'John'


def test_start_command_user_exists(mbot, start_command_update):
    User.objects.create(user_id=start_command_update.message.from_user.id, first_name='John')
    command_start(start_command_update, {})

    assert mbot.text == (
        'Welcome back, John!\n\n'
        'Remind you about the rules:\n\n'
        '• *A list:* Very important people. Contact every three weeks.\n'
        '• *B list:* Important people. Contact every two months.\n'
        '• *C list:* Most people. Contact every six months.\n'
        '• *D list:* Demoted people. Contact once a year, to make sure you still have their correct info.\n'
    )
