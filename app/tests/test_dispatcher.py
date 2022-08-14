from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler
from tgbot.dispatcher import dispatcher
from tgbot.handlers import send_stacktrace_to_tg_chat


def test_init():
    assert isinstance(dispatcher.handlers[0][0], CommandHandler)
    assert isinstance(dispatcher.handlers[0][1], CommandHandler)
    assert isinstance(dispatcher.handlers[0][2], CommandHandler)
    assert isinstance(dispatcher.handlers[0][3], CallbackQueryHandler)
    assert isinstance(dispatcher.handlers[0][4], CallbackQueryHandler)
    assert isinstance(dispatcher.handlers[0][5], MessageHandler)
    assert send_stacktrace_to_tg_chat in dispatcher.error_handlers
