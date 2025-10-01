from django.urls import path

from apps.views import ProductListView, ProductSearchView

urlpatterns = [
    path('product/list/', ProductListView.as_view(), name='product-list'),
    path('product/search/', ProductSearchView.as_view(), name='search'),
]
