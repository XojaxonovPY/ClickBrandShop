from django.urls import path
from apps.views import *

urlpatterns = [
    path('profile/', ProfileTemplateView.as_view(), name='profile'),
    path('profile/order/list/', OrdersListView.as_view(), name='order-list'),
    path('profile/address/list/', AddressListView.as_view(), name='address-list'),
    path('profile/wish/list/', WishlistListView.as_view(), name='wishlist-list'),
    path('profile/notifications/', NotificationListView.as_view(), name='profile-notifications'),
    path('profile/about-us/', AboutTemplateView.as_view(), name='profile-about'),
]

urlpatterns += [
    path('address/save/', AddressCreateView.as_view(), name='address-save'),
    path('profile/update/<int:pk>/', ProfileUpdateView.as_view(), name='update-profile'),
    path('profile/address/update/', AddressView.as_view(), name='address-update'),
    path('profile/address/delete/<int:pk>/', AddressViewDelete.as_view(), name='address-delete'),
]
