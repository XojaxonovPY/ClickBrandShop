from django.urls import path

from apps.views import *

urlpatterns = [
    path('order/item/save/', OrderItemCreateView.as_view(), name='order_item'),
    path('order/item/list/', OderItemListView.as_view(), name='item-list'),
    path('order/item/delete/<int:pk>/', OrderItemDeleteView.as_view(), name='delete-item'),
    path('order/item/update/<int:pk>/', OrderItemView.as_view(), name='update-item')
]

urlpatterns += [
    path('orders/', OrderListView.as_view(), name='orders'),
    path('orders/save', OrderCreateView.as_view(), name='orders-save'),
]
