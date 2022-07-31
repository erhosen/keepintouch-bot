import json
import logging
from pprint import pformat

from django.http import JsonResponse
from django.views import View

logger = logging.getLogger(__name__)


def process_telegram_event(event):
    logger.info(pformat(event))


class TelegramBotWebhookView(View):
    def post(self, request, *args, **kwargs):
        """
        https://github.com/ohld/django-telegram-bot/blob/main/tgbot/views.py
        WARNING: if fail - Telegram webhook will be delivered again.
        """
        body = json.loads(request.body)

        process_telegram_event(body)

        message = body["message"]
        chat_id = message["chat"]["id"]

        text = "I will answer u someday"

        msg = {
            "method": "sendMessage",
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown",
            "reply_to_message_id": message["message_id"],
        }

        return JsonResponse(msg)
