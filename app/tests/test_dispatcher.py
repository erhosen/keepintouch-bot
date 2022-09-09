import pytest
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler
from tgbot.dispatcher import Unauthenticated, dispatcher
from tgbot.handlers.special import send_stacktrace_to_tg_chat


def test_init():
    assert isinstance(dispatcher.handlers[0][0], CommandHandler)
    assert isinstance(dispatcher.handlers[0][1], CommandHandler)
    assert isinstance(dispatcher.handlers[0][2], CommandHandler)
    assert isinstance(dispatcher.handlers[0][3], CommandHandler)
    assert isinstance(dispatcher.handlers[0][4], CallbackQueryHandler)
    assert isinstance(dispatcher.handlers[0][5], CallbackQueryHandler)
    assert isinstance(dispatcher.handlers[0][6], CallbackQueryHandler)
    assert isinstance(dispatcher.handlers[0][7], MessageHandler)
    assert send_stacktrace_to_tg_chat in dispatcher.error_handlers


def test_process_telegram_event_from_owner(telegram_message_update):
    from tgbot.dispatcher import process_telegram_event

    process_telegram_event(telegram_message_update.to_dict())


def test_process_telegram_event_from_stranger(telegram_message_update):
    from tgbot.dispatcher import process_telegram_event

    telegram_message_update.message.from_user.id = 7777777777
    with pytest.raises(Unauthenticated):
        process_telegram_event(telegram_message_update.to_dict())
