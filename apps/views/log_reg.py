from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, View

from apps.forms import RegisterForm


class RegisterFormView(FormView):
    form_class = RegisterForm
    template_name = 'login-register/register.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        user = form.user
        login(self.request, user)
        return super().form_valid(form)


class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('main')