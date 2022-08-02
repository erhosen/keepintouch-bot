from queue import Queue

from django.conf import settings
from telegram import Bot, BotCommand, Update
from telegram.ext import CallbackQueryHandler, CommandHandler, Dispatcher, Filters, MessageHandler
from tgbot.handlers import contacts, notification, start, utils

# Global variable - the best way I found to init Telegram bot

bot = Bot(settings.TELEGRAM_TOKEN)


def process_telegram_event(update_json):
    update = Update.de_json(update_json, bot)
    dispatcher.process_update(update)


def setup_dispatcher(dp):
    """
    Adding handlers for events from Telegram
    """
    # onboarding
    dp.add_handler(CommandHandler("start", start.command_start))

    # Add Contact Flow
    dp.add_handler(CommandHandler("add_contact", contacts.add_contact))
    dp.add_handler(MessageHandler(Filters.contact, contacts.shared_contact_handler))
    dp.add_handler(CallbackQueryHandler(contacts.set_group_handler, pattern=f'^{contacts.SET_GROUP_MARKER}'))

    # List of contacts
    dp.add_handler(CommandHandler("list", contacts.list_contacts))

    # Handle KeepInTouch Notifications
    dp.add_handler(
        CallbackQueryHandler(notification.handle_keepintouch_callback, pattern=f'^{notification.KEEPINTOUCH_MARKER}')
    )

    # handling errors
    dp.add_error_handler(utils.send_stacktrace_to_tg_chat)

    return dp


def set_up_commands(bot_instance: Bot) -> None:
    commands = {
        'start': 'Start KeepInTouch bot 🚀',
        'add_contact': 'Share a contact 👤',
        'list': 'Show contacts ℹ️',
    }

    bot_instance.delete_my_commands()
    bot_instance.set_my_commands(
        commands=[BotCommand(command, description) for command, description in commands.items()]
    )


if not settings.DEBUG:
    # WARNING: it's better to comment the line below in DEBUG mode.
    # Likely, you'll get a flood limit control error, when restarting bot too often
    set_up_commands(bot)

queue: Queue = Queue()
dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=queue, workers=1, use_context=True))
