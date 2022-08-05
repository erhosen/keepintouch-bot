# Keepintouch-bot

### Keepintouch-bot is a bot that keeps you in touch with your friends.

_____

<img align="left" width="350" src="img/demo.png">

Based on article ["Stay in touch with hundreds of people"](https://sive.rs/hundreds) by [Derek Sivers](https://sive.rs/).

Runs on [Yandex.Cloud Functions](https://cloud.yandex.com/en/docs/functions/) or any other serverless platform.

The bot handles POST requests triggered by [Telegram Webhooks](https://core.telegram.org/bots/api#setwebhook).

Also, it triggered by [Yandex.Cloud Triggers](https://cloud.yandex.com/en/docs/functions/quickstart/create-trigger/timer-quickstart) once a day to check, if it's time to write a message to your friends.

Uses Django Framework, without all unnecessary features. Some ideas how to make it fast and lightweight are taken from [serverless-micro-django](https://github.com/mmoallemi99/serverless-micro-django)

## Deployment:

Three steps of CI:
* lint (black, flake8, isort, mypy) — code quality check
* test — python tests
* deploy — actual deployment using [Yandex-Serveless-Action](https://github.com/goodsmileduck/yandex-serverless-action)

For more information, see [workflow](/.github/workflows/main.yml)

## Development

The only way to develop a new features for Telegram bot is writing [tests](/app/tests/).

```bash
make test
```
