from django.core.management.base import BaseCommand
from django.utils import timezone
import logging


from tgbot.handlers.notification import keyboard_notification_choices
from tgbot.models import User
from tgbot.dispatcher import bot

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    command_name = "notify_keepintouch"

    def send_message(self, user, contact):
        text = f"""
It's time to write a few words to {contact.linkable_name}!

Last time you wrote to them {contact.last_contact_date_humanized}"""
        bot.send_message(user.user_id, text, parse_mode="Markdown", reply_markup=keyboard_notification_choices(contact.id))

    def handle(self, *args, **options):
        logger.info(f"Start {self.command_name}")

        today = timezone.now().date()
        for user in User.objects.all().prefetch_related('contacts'):
            for contact in user.contacts.all():
                if contact.next_contact_date <= today:
                    logger.info(f"It's time for {user} write a few words to {contact}")
                    self.send_message(user, contact)

        logger.info(f"End of {self.command_name}")
