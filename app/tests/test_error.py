import pytest
from tgbot.handlers import send_stacktrace_to_tg_chat


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

    assert mbot.chat_id == settings.TELEGRAM_LOGS_CHAT_ID
    assert mbot.text == (
        '⚠️⚠️⚠️ for @jdoe:\n'
        'An exception was raised while handling an update\n'
        '<pre>Exception: error occurred\n'
        '</pre>'
    )
