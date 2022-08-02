from django.utils import timezone
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

from tgbot.models import Contact

KEEPINTOUCH_MARKER = "KEEPINTOUCH"


def keyboard_notification_choices(contact_id: int) -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton("Ok", callback_data=f'{KEEPINTOUCH_MARKER}:{contact_id}:0'),
        InlineKeyboardButton("Tomorrow", callback_data=f'{KEEPINTOUCH_MARKER}:{contact_id}:1'),
        InlineKeyboardButton("In a week", callback_data=f'{KEEPINTOUCH_MARKER}:{contact_id}:7'),
        InlineKeyboardButton("Demote", callback_data=f'{KEEPINTOUCH_MARKER}:{contact_id}:-1'),
    ]]

    return InlineKeyboardMarkup(buttons)


def keepintouch_decision_handler(update: Update, context: CallbackContext) -> None:
    _, contact_id, choice = update.callback_query.data.split(':')
    contact = Contact.objects.get(id=contact_id)
    today = timezone.now().date()
    if choice == '0':
        contact.last_contact_date = today
        contact.save()
        text = f"Contact {contact.full_name} marked as contacted! Next notification will be sent {contact.next_contact_date_humanized}"
    elif choice == '1':
        contact.last_contact_date = today + timezone.timedelta(days=1)
        contact.save()
        text = f"I will notify you again tomorrow about {contact.full_name}!"
    elif choice == '7':
        contact.last_contact_date = today + timezone.timedelta(days=7)
        contact.save()
        text = f"I will notify you again in a week about {contact.full_name}!"
    elif choice == '-1':
        contact.demote()
        contact.save()
        text = f"Contact {contact.full_name} was demoted to group {contact.group}"
    else:
        text = f"Unknown choice {choice}"

    update.callback_query.edit_message_text(text=text)
