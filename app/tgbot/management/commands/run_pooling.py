import logging

from django.core.management.base import BaseCommand
from tgbot.dispatcher import run_pooling

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    command_name = "run_pooling"

    def handle(self, *args, **options):
        run_pooling()
        logger.info("!!! Do not forget to set up correct webhook in production !!!")
