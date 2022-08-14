import logging

import telegram
from django.conf import settings
from django.core.management.base import BaseCommand
from tgbot.handlers.notification import run_notify_keepintouch

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    command_name = "notify_keepintouch"

    def handle(self, *args, **options):
        logger.info(f"Start {self.command_name}")

        bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)
        stats = run_notify_keepintouch(bot)
        logger.info(f"Checked {stats['total']} contacts, sent {stats['sent']} messages")

        logger.info(f"End of {self.command_name}")
