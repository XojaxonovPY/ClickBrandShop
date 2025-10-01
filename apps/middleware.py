# yourapp/middleware.py
from django.utils import translation
from apps.models import TelegramUser


class TelegramLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/telegram-login/"):
            return self.get_response(request)

        if hasattr(request, 'LANGUAGE_CODE'):
            print("Django til aktiv:", request.LANGUAGE_CODE)
            return self.get_response(request)

        telegram_id = request.session.get('telegram_id')
        print("Sessiondan olingan telegram_id:", telegram_id)

        if telegram_id:
            try:
                # 🛠 KELADIGAN XATO SHU YERDA
                user = TelegramUser.objects.get(user_id=telegram_id)
                lang = user.language_code
                translation.activate(lang)
                request.LANGUAGE_CODE = lang
                print("Telegram foydalanuvchi tili faollashtirildi:", lang)
            except TelegramUser.DoesNotExist:
                print("Telegram foydalanuvchi topilmadi!")
            except Exception as e:
                print("XATOLIK:", e)

        return self.get_response(request)
