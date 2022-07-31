from collections import defaultdict

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

from tgbot.core import Group
from tgbot.models import Contact, User

SHARE_CONTACT_TUTOR_IMG = 'https://www.wikihow.com/images/thumb/a/a1/Find-Contacts-on-Telegram-on-Android-Step-15.jpg/v4-460px-Find-Contacts-on-Telegram-on-Android-Step-15.jpg'
SET_GROUP_MARKER = 'SET_GROUP'


def add_contact(update: Update, context: CallbackContext) -> None:
    caption = "Share your contact with me\n\nBTW, you can do it without /add_contact"
    update.message.reply_photo(SHARE_CONTACT_TUTOR_IMG, caption=caption)


def keyboard_choose_group(contact_id: int) -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton("A", callback_data=f'{SET_GROUP_MARKER}:{contact_id}:A'),
        InlineKeyboardButton("B", callback_data=f'{SET_GROUP_MARKER}:{contact_id}:B'),
        InlineKeyboardButton("C", callback_data=f'{SET_GROUP_MARKER}:{contact_id}:C'),
        InlineKeyboardButton("D", callback_data=f'{SET_GROUP_MARKER}:{contact_id}:D')
    ]]

    return InlineKeyboardMarkup(buttons)


def shared_contact_handler(update: Update, context: CallbackContext) -> None:
    user = User.get_user(update, context)

    contact, _ = Contact.objects.get_or_create(
        telegram_id=update.message.contact.user_id,
        phone_number=update.message.contact.phone_number,
        user=user,
        defaults={
            'first_name': update.message.contact.first_name,
            'last_name': update.message.contact.last_name,
            'group': Group.C,
        }
    )

    text = f"What group do you want to add {contact.full_name} to? \n\n" \
           f"The rules are simple: \n" \
           f"• *A list:* Very important people. Contact every three weeks.\n" \
           f"• *B list:* Important people. Contact every two months.\n" \
           f"• *C list:* Most people. Contact every six months.\n" \
           f"• *D list:* Demoted people. Contact once a year, to make sure you still have their correct info."

    update.message.reply_markdown(text, reply_markup=keyboard_choose_group(contact.id))


def set_group_handler(update: Update, context: CallbackContext) -> None:
    _, contact_id, group = update.callback_query.data.split(':')
    contact = Contact.objects.get(id=contact_id)
    contact.group = group
    contact.save()

    update.callback_query.edit_message_text(
        text=f"{contact.full_name} is now in {contact.group} list"
    )


def list_contacts(update: Update, context: CallbackContext) -> None:
    """
    Your contacts:

        List A
        Алекс Шмитько (tg://openmessage?user_id=34513223) | July 30, 2022

        List B
        Семен Тарасов (tg://openmessage?user_id=0) | September 11, 2022
        Кирилл Магистратура (tg://openmessage?user_id=143131035) | September 7, 2022

        List C
        Ivan Chernov (tg://openmessage?user_id=112776829) | January 5, 2023

        List D
        Anton Ogorodnikov (tg://openmessage?user_id=43125388) | July 9, 2023
    """
    user = User.get_user(update, context)
    contacts = Contact.objects.filter(user=user)

    group_to_contacts = defaultdict(list)
    for contact in contacts:
        group_to_contacts[contact.group].append(contact)

    text = f"Here are your contacts:\n\n"
    for group in Group:
        text += f"*List {group}:*\n"
        for contact in group_to_contacts[group]:
            text += f"{contact.full_name} - {contact.next_contact_date} - {contact.group}\n"
        text += "\n"

    update.message.reply_markdown(text)
