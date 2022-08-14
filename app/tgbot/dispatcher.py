import logging
from queue import Queue

from django.conf import settings
from telegram import Bot, BotCommand, Update
from telegram.ext import CallbackQueryHandler, CommandHandler, Dispatcher, Filters, MessageHandler
from tgbot import handlers
from tgbot.core import CallbackMarker


def process_telegram_event(update_json):
    update = Update.de_json(update_json, bot)
    if update.effective_user.id == settings.TELEGRAM_ID:
        dispatcher.process_update(update)
    else:
        logging.info(f"Ignoring update from {update.effective_user}")
        raise ValueError("Update is not from bot owner!")


def setup_dispatcher(dp: Dispatcher) -> Dispatcher:
    """
    Adding handlers for events from Telegram
    """
    # Commands
    dp.add_handler(CommandHandler("start", handlers.command_start))
    dp.add_handler(CommandHandler("add_contact", handlers.command_add_contact))
    dp.add_handler(CommandHandler("list", handlers.command_list))

    # Callbacks
    dp.add_handler(CallbackQueryHandler(handlers.callback_set_group, pattern=f'^{CallbackMarker.SET_GROUP}'))
    dp.add_handler(CallbackQueryHandler(handlers.callback_keepintouch, pattern=f'^{CallbackMarker.KEEPINTOUCH}'))

    # Messages
    dp.add_handler(MessageHandler(Filters.contact, handlers.message_shared_contact))

    # Errors
    dp.add_error_handler(handlers.send_stacktrace_to_tg_chat)

    return dp


def set_up_commands(bot_instance: Bot) -> None:
    commands = {
        "start": "Start KeepInTouch bot 🚀",
        "add_contact": "Share a contact 👤",
        "list": "Show contacts ℹ️",
    }

    bot_instance.delete_my_commands()
    bot_instance.set_my_commands(
        commands=[BotCommand(command, description) for command, description in commands.items()]
    )


bot = Bot(settings.TELEGRAM_TOKEN)
dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=Queue(), workers=1, use_context=True))
