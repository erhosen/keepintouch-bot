import telegram
from django.utils import timezone
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext
from tgbot.core import CallbackMarker, KeepintouchChoices
from tgbot.models import Contact, User


def keyboard_notification_choices(contact_id: int) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                "Ok", callback_data=f'{CallbackMarker.KEEPINTOUCH}:{contact_id}:{KeepintouchChoices.OK}'
            ),
            InlineKeyboardButton(
                "Tomorrow", callback_data=f'{CallbackMarker.KEEPINTOUCH}:{contact_id}:{KeepintouchChoices.TOMORROW}'
            ),
            InlineKeyboardButton(
                "In a week", callback_data=f'{CallbackMarker.KEEPINTOUCH}:{contact_id}:{KeepintouchChoices.IN_A_WEEK}'
            ),
            InlineKeyboardButton(
                "Demote", callback_data=f'{CallbackMarker.KEEPINTOUCH}:{contact_id}:{KeepintouchChoices.DEMOTE}'
            ),
        ]
    ]

    return InlineKeyboardMarkup(buttons)


def send_notification_message(bot: telegram.Bot, user: User, contact: Contact) -> None:
    text = (
        f"💬 It's time to write a few words to {contact.linkable_name} \n\n"
        f"Last time you contacted *{contact.last_contact_date_humanized}* (List {contact.group})\n"
    )
    bot.send_message(
        chat_id=user.user_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboard_notification_choices(contact.id),
    )


def callback_keepintouch(update: Update, context: CallbackContext) -> None:
    _, contact_id, raw_choice = update.callback_query.data.split(':')
    choice = KeepintouchChoices(raw_choice)
    contact = Contact.objects.get(id=contact_id)
    text = "..."
    if choice == KeepintouchChoices.OK:
        contact.last_contact_date = timezone.now().date()
        contact.save(update_fields=['last_contact_date'])
        text = f"Well done 👍\nNext notification will be in {contact.next_contact_date_humanized} from now"
    elif choice == KeepintouchChoices.TOMORROW:
        contact.last_contact_date += timezone.timedelta(days=1)
        contact.save(update_fields=['last_contact_date'])
        text = f"I'll notify you again in {contact.next_contact_date_humanized} 👌"
    elif choice == KeepintouchChoices.IN_A_WEEK:
        contact.last_contact_date += timezone.timedelta(days=7)
        contact.save(update_fields=['last_contact_date'])
        text = f"I'll notify you again in {contact.next_contact_date_humanized} 👌"
    elif choice == KeepintouchChoices.DEMOTE:
        try:
            contact.demote()
            text = (
                f"Contact {contact.linkable_name} was demoted to *group {contact.group}*\n"
                f"I'll notify you again in {contact.next_contact_date_humanized} 👌"
            )
        except ValueError:
            contact.delete()
            text = f"Contact {contact.linkable_name} deleted.\nNo more notifications for this contact. 😢"

    update.callback_query.edit_message_text(text=text, parse_mode=ParseMode.MARKDOWN)
