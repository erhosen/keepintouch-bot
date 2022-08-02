import json
import logging

from django.http import JsonResponse
from django.views import View
from tgbot.dispatcher import process_telegram_event

logger = logging.getLogger(__name__)


class TelegramBotWebhookView(View):
    def post(self, request, *args, **kwargs):
        """
        https://github.com/ohld/django-telegram-bot/blob/main/tgbot/views.py
        WARNING: if fail - Telegram webhook will be delivered again.
        """
        body = json.loads(request.body)

        process_telegram_event(body)

        return JsonResponse({"ok": "POST request processed"})
