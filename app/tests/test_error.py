from telegram import Update
from tgbot.handlers import send_stacktrace_to_tg_chat


def test_error_handler(command_list_json, mbot, callback_context):
    from django.conf import settings

    update = Update.de_json(command_list_json, mbot)
    send_stacktrace_to_tg_chat(update, callback_context)

    assert mbot.chat_id == settings.TELEGRAM_LOGS_CHAT_ID
    assert mbot.parse_mode == 'HTML'
    assert mbot.text == (
        '⚠️⚠️⚠️ for @jdoe:\n'
        'An exception was raised while handling an update\n'
        '<pre>Exception: error occurred\n'
        '</pre>'
    )
