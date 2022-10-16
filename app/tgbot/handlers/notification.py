import telegram
from django.db import transaction
from django.utils import timezone
from telegram import ParseMode
from tgbot.models import Contact, User


@transaction.atomic
def notify_user(bot: telegram.Bot, user: User, contact: Contact) -> None:
    text = (
        f"💬 It's time to write a few words to {contact.linkable_name} \n\n"
        f"Last time you contacted *{contact.last_contact_date_humanized}* (List {contact.group})\n"
    )
    bot.send_message(
        chat_id=user.user_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
    )
    contact.last_contact_date = timezone.now().date()
    contact.save(update_fields=['last_contact_date'])


def run_notify_keepintouch(bot: telegram.Bot) -> dict:
    today = timezone.now().date()
    stats = {'total': 0, 'sent': 0}
    for user in User.objects.all().prefetch_related('contacts'):
        for contact in user.contacts.all():
            stats['total'] += 1
            if contact.next_contact_date <= today:
                notify_user(bot, user, contact)
                stats['sent'] += 1
    return stats
