from collections import defaultdict

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from tgbot.core import KEEPINTOUCH_RULES, SHARE_CONTACT_TUTOR_IMG, CallbackMarker, Group
from tgbot.models import Contact, User


def command_add_contact(update: Update, context: CallbackContext) -> None:
    caption = "Share your contact with me\n\nBTW, you can do it without /add_contact"
    update.message.reply_photo(SHARE_CONTACT_TUTOR_IMG, caption=caption)


def keyboard_choose_group(contact_id: int) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton("A", callback_data=f'{CallbackMarker.SET_GROUP}:{contact_id}:{Group.A}'),
            InlineKeyboardButton("B", callback_data=f'{CallbackMarker.SET_GROUP}:{contact_id}:{Group.B}'),
            InlineKeyboardButton("C", callback_data=f'{CallbackMarker.SET_GROUP}:{contact_id}:{Group.C}'),
            InlineKeyboardButton("D", callback_data=f'{CallbackMarker.SET_GROUP}:{contact_id}:{Group.D}'),
        ]
    ]

    return InlineKeyboardMarkup(buttons)


def message_shared_contact(update: Update, context: CallbackContext) -> None:
    user = User.get_user(update, context)

    contact, _ = Contact.objects.get_or_create(
        telegram_id=update.message.contact.user_id,
        phone_number=update.message.contact.phone_number,
        user=user,
        defaults={
            'first_name': update.message.contact.first_name,
            'last_name': update.message.contact.last_name,
            'group': Group.C,
        },
    )

    text = f"What group do you want to add {contact.full_name} to? \n\nThe rules are simple: \n{KEEPINTOUCH_RULES}"
    update.message.reply_markdown(text, reply_markup=keyboard_choose_group(contact.id))


def callback_set_group(update: Update, context: CallbackContext) -> None:
    _, contact_id, raw_group = update.callback_query.data.split(':')
    contact = Contact.objects.get(id=contact_id)
    contact.group = Group[raw_group]
    contact.save()

    update.callback_query.edit_message_text(text=f"{contact.full_name} is now in {contact.group} list")


def command_list(update: Update, context: CallbackContext) -> None:
    user = User.get_user(update, context)
    contacts = Contact.objects.filter(user=user)

    group_to_contacts = defaultdict(list)
    for contact in contacts:
        group_to_contacts[contact.group].append(contact)

    text = "Here are your contacts:\n\n"
    for group in Group:
        text += f"*List {group}:*\n"
        for contact in group_to_contacts[group]:
            text += f"{contact.linkable_name} | {contact.next_contact_date_humanized}\n"
        text += "\n"

    update.message.reply_markdown(text)
