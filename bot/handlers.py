from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, WebAppInfo, InlineKeyboardButton
from aiogram.utils.keyboard import KeyboardButton

from bot.functions import save_user, reply_button_builder, send_language_to_backend, inline_button_builder

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    user = {
        'user_id': message.from_user.id,
        'username': message.from_user.username,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name,
    }
    await save_user(**user)
    buttons = [
        KeyboardButton(text="Do'kon", web_app=WebAppInfo(url='https://debt-book.onrender.com/')),
        KeyboardButton(text="Tilni o'zgartitish"),
        KeyboardButton(text='Mening buyurtmalarim', web_app=WebAppInfo(url='https://clickbrandshop.robostore.uz/'))
    ]
    markup = await reply_button_builder(buttons, [1])
    text = f"Assalomu alaykum{user['first_name']},Click Brandshop botiga xush kelibsiz!"
    await message.answer(text, reply_markup=markup)


@router.message(F.text == "Tilni o'zgartitish")
async def echo(message: Message):
    buttons = [
        KeyboardButton(text="🇺🇿 O'zbek tili"),
        KeyboardButton(text="🇷🇺 Русский язык"),
    ]
    markup = await reply_button_builder(buttons, [1])
    await message.answer(message.text, reply_markup=markup)


@router.message(F.text.in_({"🇺🇿 O'zbek tili", "🇷🇺 Русский язык"}))
async def set_language(message: Message):
    user_id = message.from_user.id

    if message.text == "🇺🇿 O'zbek tili":
        lang_code = "uz"
        msg = "Til o'zgartirildi: O'zbek tili 🇺🇿"
    elif message.text == "🇷🇺 Русский язык":
        lang_code = "ru"
        msg = "Язык изменен: Русский язык 🇷🇺"
    else:
        lang_code = "uz"
        msg = "Standart til: O'zbek"
    success = send_language_to_backend(user_id, lang_code)
    if success:
        await message.answer(text=msg)
        await message.answer(
            f"[🔗 Saytga kirish](http://127.0.0.1:8000/telegram-login/?telegram_id={user_id})",
            parse_mode="MarkdownV2"
        )

    else:
        await message.answer("Tilni saqlashda xatolik yuz berdi.")
