import pytest
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler
from tgbot.dispatcher import Unauthenticated, dispatcher
from tgbot.handlers.error import send_stacktrace_to_tg_chat


def test_init():
    assert isinstance(dispatcher.handlers[0][0], CommandHandler)
    assert isinstance(dispatcher.handlers[0][1], CommandHandler)
    assert isinstance(dispatcher.handlers[0][2], CommandHandler)
    assert isinstance(dispatcher.handlers[0][3], CallbackQueryHandler)
    assert isinstance(dispatcher.handlers[0][4], CallbackQueryHandler)
    assert isinstance(dispatcher.handlers[0][5], MessageHandler)
    assert send_stacktrace_to_tg_chat in dispatcher.error_handlers


def test_process_telegram_event_from_owner(telegram_message_update):
    from tgbot.dispatcher import process_telegram_event

    process_telegram_event(telegram_message_update.to_dict())


def test_process_telegram_event_from_stranger(telegram_message_update):
    from tgbot.dispatcher import process_telegram_event

    telegram_message_update.message.from_user.id = 7777777777
    with pytest.raises(Unauthenticated):
        process_telegram_event(telegram_message_update.to_dict())


def test_set_up_commands(mbot):
    from tgbot.dispatcher import set_up_commands

    set_up_commands(mbot)

    assert mbot.commands[0].command == "start"
    assert mbot.commands[0].description == "Start KeepInTouch bot 🚀"
    assert mbot.commands[1].command == "add_contact"
    assert mbot.commands[1].description == "Share a contact 👤"
    assert mbot.commands[2].command == "list"
    assert mbot.commands[2].description == "Show contacts ℹ️"
