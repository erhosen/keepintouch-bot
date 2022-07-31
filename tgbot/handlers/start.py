import logging
from pprint import pformat

from telegram import Update
from telegram.ext import CallbackContext

from tgbot.models import User

logger = logging.getLogger(__name__)


def command_start(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)

    if created:
        text = "Sup, {first_name}!".format(first_name=u.first_name)
    else:
        text = "Welcome back, {first_name}!".format(first_name=u.first_name)

    update.message.reply_text(text=text)
