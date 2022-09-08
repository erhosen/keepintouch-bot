import logging
from queue import Queue

from django.conf import settings
from telegram import Bot, Update
from telegram.ext import CallbackQueryHandler, CommandHandler, Dispatcher, Filters, MessageHandler, Updater
from tgbot.core import CallbackMarker
from tgbot.handlers import contacts as contacts_handlers
from tgbot.handlers import notification as notification_handlers
from tgbot.handlers import start as start_handlers
from tgbot.handlers.special import send_stacktrace_to_tg_chat


class Unauthenticated(Exception):
    pass


def process_telegram_event(update_json):
    update = Update.de_json(update_json, bot)
    if update.effective_user.id == settings.TELEGRAM_ID:
        dispatcher.process_update(update)
    else:
        logging.warning(f"Received update from unauthenticated user {update.effective_user.id}")
        raise Unauthenticated("Not bot owner")


def setup_dispatcher(dp: Dispatcher) -> Dispatcher:
    """
    Adding handlers for events from Telegram
    """
    # Commands
    dp.add_handler(CommandHandler("start", start_handlers.command_start))
    dp.add_handler(CommandHandler("add_contact", contacts_handlers.command_add_contact))
    dp.add_handler(CommandHandler("list", contacts_handlers.command_list))

    # Callbacks
    dp.add_handler(CallbackQueryHandler(contacts_handlers.callback_set_group, pattern=f'^{CallbackMarker.SET_GROUP}'))
    dp.add_handler(
        CallbackQueryHandler(notification_handlers.callback_keepintouch, pattern=f'^{CallbackMarker.KEEPINTOUCH}')
    )

    # Messages
    dp.add_handler(MessageHandler(Filters.contact, contacts_handlers.message_shared_contact))

    # Errors
    dp.add_error_handler(send_stacktrace_to_tg_chat)

    return dp


def run_pooling():
    """Run bot in pooling mode"""
    updater = Updater(settings.TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot_info = Bot(settings.TELEGRAM_TOKEN).get_me()
    bot_link = f"https://t.me/{bot_info['username']}"

    print(f"Pooling of '{bot_link}' started")
    # it is really useful to send '👋' emoji to developer, when you run local test
    bot.send_message(text='👋', chat_id=settings.TELEGRAM_ID)

    updater.start_polling()
    updater.idle()


bot = Bot(settings.TELEGRAM_TOKEN)
dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=Queue(), workers=1, use_context=True))
