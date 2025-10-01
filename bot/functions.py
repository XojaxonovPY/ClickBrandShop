import os

from asgiref.sync import sync_to_async
from django.views.decorators.csrf import csrf_exempt

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')

import django

django.setup()
import requests
from apps.models import TelegramUser
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


@sync_to_async
def save_user(**kwargs):
    query = TelegramUser.objects.filter(user_id=kwargs['user_id'])
    if not query.exists():
        TelegramUser.objects.create(**kwargs)


async def reply_button_builder(buttons: list, size=(1,), one_time=False):
    rkb = ReplyKeyboardBuilder()
    rkb.add(*buttons)
    rkb.adjust(*size)
    rkb = rkb.as_markup(resize_keyboard=True)
    return rkb


async def inline_button_builder(buttons: list, size=(1,), one_time=False):
    inline = InlineKeyboardBuilder()
    inline.add(*buttons)
    inline.adjust(*size)
    inline = inline.as_markup(resize_keyboard=True)
    return inline


@csrf_exempt
def send_language_to_backend(telegram_id: int, language_code: str):
    url = "http://localhost:8000/ru/set-language/"
    data = {
        "telegram_id": telegram_id,
        "language": language_code
    }
    try:
        response = requests.post(url, json=data)
        return response.ok
    except Exception as e:
        print("Error sending language:", e)
        return False
