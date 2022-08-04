from telegram import Update
from tgbot.handlers import command_start
from tgbot.models import User


def test_start_command_new_user(mbot, start_command_json):
    update = Update.de_json(start_command_json, mbot)
    command_start(update, {})

    assert mbot.text == 'Sup, John!'
    assert User.objects.get(user_id=999999999).first_name == 'John'


def test_start_command_user_exists(mbot, start_command_json):
    user_id = start_command_json['message']['from']['id']
    User.objects.create(user_id=user_id, first_name='John')
    update = Update.de_json(start_command_json, mbot)
    command_start(update, {})

    assert mbot.text == (
        'Welcome back, John!\n\n'
        'Remind you about the rules:\n\n'
        '• *A list:* Very important people. Contact every three weeks.\n'
        '• *B list:* Important people. Contact every two months.\n'
        '• *C list:* Most people. Contact every six months.\n'
        '• *D list:* Demoted people. Contact once a year, to make sure you still have their correct info.\n'
    )
