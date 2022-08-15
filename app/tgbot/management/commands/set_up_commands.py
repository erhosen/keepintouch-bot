import logging

import telegram
from django.conf import settings
from django.core.management.base import BaseCommand
from tgbot.handlers.special import set_up_commands

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    command_name = "set_up_commands"

    def handle(self, *args, **options):
        logger.info(f"Start {self.command_name}")

        bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)
        set_up_commands(bot)

        logger.info(f"End of {self.command_name}")
