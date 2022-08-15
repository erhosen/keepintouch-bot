import pytest
from tgbot.handlers.special import send_stacktrace_to_tg_chat, set_up_commands


@pytest.fixture
def callback_context(mbot):
    class CallbackContext:
        @property
        def error(self):
            return Exception('error occurred')

        @property
        def bot(self):
            return mbot

    return CallbackContext()


def test_error_handler(telegram_message_update, mbot, callback_context):
    from django.conf import settings

    send_stacktrace_to_tg_chat(telegram_message_update, callback_context)

    assert mbot.chat_id == settings.TELEGRAM_ID
    assert mbot.text == (
        '⚠️⚠️⚠️ for @jdoe:\n'
        'An exception was raised while handling an update\n'
        '<pre>Exception: error occurred\n'
        '</pre>'
    )


def test_set_up_commands(mbot):
    set_up_commands(mbot)

    assert mbot.commands[0].command == "start"
    assert mbot.commands[0].description == "Start KeepInTouch bot 🚀"
    assert mbot.commands[1].command == "add_contact"
    assert mbot.commands[1].description == "Share a contact 👤"
    assert mbot.commands[2].command == "list"
    assert mbot.commands[2].description == "Show contacts ℹ️"
