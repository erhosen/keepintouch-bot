import html
import logging
import traceback

import telegram
from django.conf import settings
from telegram import Bot, BotCommand, Update
from telegram.ext import CallbackContext
from tgbot.models import User


def send_stacktrace_to_tg_chat(update: Update, context: CallbackContext) -> None:
    u = User.get_user(update, context)

    logging.error("Exception while handling an update:", exc_info=context.error)

    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    message = f'An exception was raised while handling an update\n' f'<pre>{html.escape(tb_string)}</pre>'

    user_message = """
😔 Something broke inside the bot.
It is because we are constantly improving our service but sometimes we might forget to test some basic stuff.
We already received all the details to fix the issue.
Return to /start
"""
    context.bot.send_message(
        chat_id=u.user_id,
        text=user_message,
    )

    admin_message = f"⚠️⚠️⚠️ for {u.tg_str}:\n{message}"[:4090]
    context.bot.send_message(
        chat_id=settings.TELEGRAM_ID,
        text=admin_message,
        parse_mode=telegram.ParseMode.HTML,
    )


def set_up_commands(bot_instance: Bot) -> None:
    commands = {
        "start": "Start KeepInTouch bot 🚀",
        "add_contact": "Share a contact 👤",
        "list": "Show contacts ℹ️",
        "list_old": "Show old list of contacts 📜",
    }

    bot_instance.delete_my_commands()
    bot_instance.set_my_commands(
        commands=[BotCommand(command, description) for command, description in commands.items()],
        scope=telegram.BotCommandScopeChat(chat_id=settings.TELEGRAM_ID),
    )
