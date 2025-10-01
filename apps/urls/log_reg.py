from django.urls import path

from apps.views import RegisterFormView, LogoutView

urlpatterns = [
    path('register/', RegisterFormView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout')
]
