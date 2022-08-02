from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from app.tgbot import views

urlpatterns = [
    path('super_secter_webhook/', csrf_exempt(views.TelegramBotWebhookView.as_view())),
]
