#!/usr/bin/env python
import json
import os
import sys


def main():
    """Run administrative tasks. Local development only."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def handler(event, context):
    """Handle lambda call"""
    import dotenv

    dotenv.read_dotenv()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    os.environ.setdefault('DATABASE_PASSWORD', context.token["access_token"])  # iam_token is database password`

    import django

    django.setup()

    if event.get("body"):
        # Handle telegram webhook call
        body = json.loads(event["body"])
        from tgbot.dispatcher import Unauthenticated, process_telegram_event

        try:
            process_telegram_event(body)
        except Unauthenticated:
            pass

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({"ok": "POST request processed"}, ensure_ascii=False),
            'isBase64Encoded': False,
        }
    elif event.get("messages"):
        # Handle trigger call
        from django.core.management import call_command

        call_command("notify_keepintouch")
    else:
        raise ValueError("Unknown event")


if __name__ == '__main__':
    main()
