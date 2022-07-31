from django.db import models

from tgbot.core import Group
from utils.models import GetOrNoneManager, nb, CreateUpdateTracker


class User(CreateUpdateTracker):
    user_id = models.PositiveBigIntegerField(primary_key=True)  # telegram_id
    username = models.CharField(max_length=32, **nb)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, **nb)
    language_code = models.CharField(max_length=8, **nb)

    objects = GetOrNoneManager()  # user = User.objects.get_or_none(user_id=<some_id>)

    @property
    def tg_str(self) -> str:
        if self.username:
            return f'@{self.username}'
        return f"{self.first_name} {self.last_name}" if self.last_name else f"{self.first_name}"

    def __str__(self):
        return f'@{self.username}' if self.username is not None else f'{self.user_id}'


class Contact(CreateUpdateTracker):
    contact_id = models.PositiveBigIntegerField(primary_key=True)  # telegram_id
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, **nb)
    group = models.CharField(choices=Group.choices(), max_length=1)
