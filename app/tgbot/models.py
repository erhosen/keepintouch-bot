from __future__ import annotations

import datetime as dt
from typing import Tuple

import humanize
from django.db import models
from telegram import Update
from telegram.ext import CallbackContext
from tgbot.core import GROUP_POLICY, Group, Role
from tgbot.utils.abstract import CreateUpdateTracker
from tgbot.utils.info import extract_user_data_from_update


class User(CreateUpdateTracker):
    user_id = models.PositiveBigIntegerField(primary_key=True)  # telegram_id
    username = models.CharField(max_length=32, null=True, blank=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, null=True, blank=True)
    language_code = models.CharField(max_length=8, null=True, blank=True)

    @classmethod
    def get_user_and_created(cls, update: Update, context: CallbackContext) -> Tuple[User, bool]:
        """python-telegram-bot's Update, Context --> User instance"""
        data = extract_user_data_from_update(update)
        u, created = cls.objects.update_or_create(user_id=data["user_id"], defaults=data)
        return u, created

    @classmethod
    def get_user(cls, update: Update, context: CallbackContext) -> User:
        u, _ = cls.get_user_and_created(update, context)
        return u

    @property
    def tg_str(self) -> str:
        if self.username:
            return f'@{self.username}'
        return f"{self.first_name} {self.last_name}" if self.last_name else f"{self.first_name}"

    def __str__(self):
        return self.tg_str


class Contact(CreateUpdateTracker):
    phone_number = models.CharField(max_length=256)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, null=True, blank=True)
    telegram_id = models.PositiveBigIntegerField(null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')

    group = models.CharField(choices=Group.choices(), max_length=1, default=Group.C)
    last_contact_date = models.DateField(default=dt.date.today)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}" if self.last_name else f"{self.first_name}"

    @property
    def next_contact_date(self) -> dt.date:
        delta = GROUP_POLICY[self.group]
        return self.last_contact_date + delta

    @property
    def next_contact_date_humanized(self) -> str:
        """
        :return: Humanized string of the next contact date
        Example: "1 day", "7 days", "a month", "a year"
        """
        return humanize.naturaldelta(dt.date.today() - self.next_contact_date)

    @property
    def last_contact_date_humanized(self) -> str:
        return humanize.naturaltime(dt.date.today() - self.last_contact_date)

    @property
    def tg_link(self) -> str:
        return f'https://t.me/{self.phone_number}'

    @property
    def linkable_name(self) -> str:
        return f'[{self.full_name}]({self.tg_link})'

    def __str__(self) -> str:
        return f'{self.full_name} [{self.group}]'


class Message(CreateUpdateTracker):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')

    role = models.CharField(choices=Role.choices(), max_length=10)
    content = models.TextField()
