import logging

from telegram import Update
from telegram.ext import CallbackContext
from tgbot.core import KEEPINTOUCH_RULES
from tgbot.models import User

logger = logging.getLogger(__name__)


def command_start(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)

    if created:
        text = f"Sup, {u.first_name}!"
    else:
        text = f"Welcome back, {u.first_name}!\n\nRemind you about the rules:\n{KEEPINTOUCH_RULES}"

    update.message.reply_markdown(text=text)
