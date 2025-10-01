from django.urls import path

from apps.views import *

urlpatterns = [
    path('', HomeListView.as_view(), name='main'),
    path('product/datail/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('product/list/', ProductListView.as_view(), name='product-list'),
    path('wishlist/save/', wishlist_save, name='wishlist-save'),
    path('set-language/', set_language_from_bot, name='set_language_bot'),
    path('telegram-login/', telegram_login, name='telegram_login')
]
