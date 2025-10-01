import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from apps.models import Products, Category, Settings, Wishlist
from apps.models import TelegramUser
from django.utils import translation
from django.conf import settings


class HomeListView(ListView):
    queryset = Products.objects.all()
    template_name = 'market/home.html'
    context_object_name = 'products'

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['categories'] = Category.objects.all()
        data['setting'] = Settings.objects.first()
        if self.request.user.is_authenticated:
            wishlist_products = Wishlist.objects.filter(user=self.request.user).values_list('product_id', flat=True)
            data['wishlist_products'] = list(wishlist_products)
        return data


class ProductDetailView(DetailView):
    queryset = Products.objects.all()
    template_name = 'market/detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'pk'

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            wishlist_products = Wishlist.objects.filter(user=self.request.user).values_list('product_id', flat=True)
            data['wishlist_products'] = list(wishlist_products)
        return data


class ProductListView(ListView):
    queryset = Products.objects.all()
    template_name = 'search/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = super().get_queryset()
        category = self.request.GET.get('category')
        if category:
            query = query.filter(category__id=category)
        return query

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['categories'] = Category.objects.all()
        return data


# =========================================wishlist==================================
@require_POST
def wishlist_save(request):
    if request.user.is_authenticated:
        data = json.loads(request.body)
        product_id = data.get('product')

        try:
            product = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            return JsonResponse({'error': 'Mahsulot topilmadi'}, status=404)

        wishlist_items = Wishlist.objects.filter(user=request.user, product=product)
        if wishlist_items.exists():
            wishlist_items.delete()
            return JsonResponse({'status': 'removed'})
        else:
            Wishlist.objects.create(user=request.user, product=product)
            return JsonResponse({'status': 'added'})

    return JsonResponse({'error': 'Not authenticated'}, status=403)


# =========================================lang ==================================

@csrf_exempt
def set_language_from_bot(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            telegram_id = data.get("telegram_id")
            language = data.get("language")

            if language not in ['uz', 'ru']:
                return JsonResponse({"status": "error", "message": "Invalid language"}, status=400)

            user, _ = TelegramUser.objects.get_or_create(user_id=telegram_id)
            user.language_code = language
            user.save()

            return JsonResponse({"status": "success", "language": language})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "POST only"}, status=405)


def telegram_login(request):
    response = redirect('/')  # ⬅️ cookie shu response ga yoziladi

    telegram_id = request.GET.get('telegram_id')
    if telegram_id:
        try:
            telegram_id = int(telegram_id)
            request.session['telegram_id'] = telegram_id

            user = TelegramUser.objects.get(user_id=telegram_id)

            lang = user.language_code
            translation.activate(lang)
            request.LANGUAGE_CODE = lang

            # ✅ BU YANGI QADAM — COOKIEga yozamiz
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)

        except (ValueError, TelegramUser.DoesNotExist):
            pass

    return response
