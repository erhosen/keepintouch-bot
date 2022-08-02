from django.conf import settings
from django.utils import timezone
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import CallbackContext

from tgbot.models import Contact, User

KEEPINTOUCH_MARKER = "KEEPINTOUCH"


def keyboard_notification_choices(contact_id: int) -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton("Ok", callback_data=f'{KEEPINTOUCH_MARKER}:{contact_id}:0'),
        InlineKeyboardButton("Tomorrow", callback_data=f'{KEEPINTOUCH_MARKER}:{contact_id}:1'),
        InlineKeyboardButton("In a week", callback_data=f'{KEEPINTOUCH_MARKER}:{contact_id}:7'),
        InlineKeyboardButton("Demote", callback_data=f'{KEEPINTOUCH_MARKER}:{contact_id}:-1'),
    ]]

    return InlineKeyboardMarkup(buttons)


def send_notification_message(user: User, contact: Contact) -> None:
    from telegram import Bot, ParseMode
    bot = Bot(token=settings.TELEGRAM_TOKEN)
    text = (
        f"💬 It's time to write a few words to {contact.linkable_name} \n\n"
        f"Last time you contacted *{contact.last_contact_date_humanized}* (List {contact.group})\n"
    )
    bot.send_message(
        user.user_id,
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboard_notification_choices(contact.id)
    )


def handle_keepintouch_callback(update: Update, context: CallbackContext) -> None:
    _, contact_id, choice = update.callback_query.data.split(':')
    contact = Contact.objects.get(id=contact_id)
    if choice == '0':
        contact.last_contact_date = timezone.now().date()
        contact.save(update_fields=['last_contact_date'])
        text = f"Well done 👍\nNext notification will be in {contact.next_contact_date_humanized} from now"
    elif choice == '1':
        contact.last_contact_date += timezone.timedelta(days=1)
        contact.save(update_fields=['last_contact_date'])
        text = f"I'll notify you again in {contact.next_contact_date_humanized} 👌"
    elif choice == '7':
        contact.last_contact_date += timezone.timedelta(days=7)
        contact.save(update_fields=['last_contact_date'])
        text = f"I'll notify you again in {contact.next_contact_date_humanized} 👌"
    elif choice == '-1':
        try:
            contact.demote()
            text = (
                f"Contact {contact.linkable_name} was demoted to *group {contact.group}*\n"
                f"I'll notify you again in {contact.next_contact_date_humanized} 👌"
            )
        except ValueError:
            contact.delete()
            text = f"Contact {contact.linkable_name} deleted.\nNo more notifications for this contact. 😢"
    else:
        text = f"Unknown choice {choice}"

    update.callback_query.edit_message_text(text=text, parse_mode=ParseMode.MARKDOWN)
