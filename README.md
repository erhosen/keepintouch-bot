# Keepintouch-bot

[![Build Status](https://github.com/ErhoSen/keepintouch-bot/actions/workflows/main.yml/badge.svg?branch=master&event=push)](https://github.com/ErhoSen/keepintouch-bot/actions?query=workflow%3ABuild+branch%3Amaster+event%3Apush)
[![codecov](https://codecov.io/gh/ErhoSen/keepintouch-bot/branch/master/graph/badge.svg?token=1FUHWGCEMA)](https://codecov.io/gh/ErhoSen/keepintouch-bot)
[![license](https://img.shields.io/github/license/erhosen/keepintouch-bot.svg)](https://github.com/ErhoSen/keepintouch-bot/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Webhook-based telegram bot, that helps you stay in touch with hundreds of people

Based on article ["Stay in touch with hundreds of people"](https://sive.rs/hundreds) by [Derek Sivers](https://sive.rs/).

## How it works

<img align="center" width="500" src="img/demo.png">

* Share Contact with the bot
* Choose a Group (A, B, C or D) for the contact
* Bot will notify you when it's time to write a message to the contact


## How it's built

Runs on [Yandex.Cloud Functions](https://cloud.yandex.com/en/docs/functions/) or any other serverless platform.

The bot handles POST requests triggered by [Telegram Webhooks](https://core.telegram.org/bots/api#setwebhook).

Also, it triggered by [Yandex.Cloud Triggers](https://cloud.yandex.com/en/docs/functions/quickstart/create-trigger/timer-quickstart) once a day to check, if it's time to write a message to your contacts.

Uses Django Framework, without unnecessary features. Some ideas how to make it fast and lightweight are taken from [serverless-micro-django](https://github.com/mmoallemi99/serverless-micro-django)

## Deployment

Deployment is done via [Yandex-Serverless-Action](https://github.com/goodsmileduck/yandex-serverless-action)

For more information, see [workflow](/.github/workflows/main.yml)

## Development

The only way to develop a new features for Telegram bot is writing [tests](/app/tests/).

```bash
make test
```
