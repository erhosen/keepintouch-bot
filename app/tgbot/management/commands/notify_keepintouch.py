import logging

from django.core.management.base import BaseCommand
from django.utils import timezone
from tgbot.handlers.notification import send_notification_message
from tgbot.models import User

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    command_name = "notify_keepintouch"

    def handle(self, *args, **options):
        logger.info(f"Start {self.command_name}")

        today = timezone.now().date()
        for user in User.objects.all().prefetch_related('contacts'):
            for contact in user.contacts.all():
                if contact.next_contact_date <= today:
                    logger.info(f"It's time for {user} write a few words to {contact}")
                    send_notification_message(user, contact)

        logger.info(f"End of {self.command_name}")
