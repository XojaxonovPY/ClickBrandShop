from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, View, TemplateView, UpdateView

from apps.forms import AddressModelForm, ProfileModelForm
from apps.models import User, Order, Address, Wishlist, Notification, Settings


class ProfileTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/profile.html'
    login_url = reverse_lazy('login')


class ProfileUpdateView(UpdateView):
    queryset = User.objects.all()
    form_class = ProfileModelForm
    template_name = 'profile/profile.html'
    success_url = reverse_lazy('profile')
    pk_url_kwarg = 'pk'


# =======================================orders========================================
class OrdersListView(ListView):
    queryset = Order.objects.all()
    template_name = 'profile/orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(item__user=self.request.user)
        return query


# =============================================address================================
class AddressCreateView(CreateView):
    form_class = AddressModelForm
    template_name = 'profile/address.html'
    success_url = reverse_lazy('address-list')


class AddressListView(ListView):
    queryset = Address.objects.all()
    template_name = 'profile/address.html'
    context_object_name = 'addresses'

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(user=self.request.user)
        return query


class AddressViewDelete(DeleteView):
    queryset = Address.objects.all()
    template_name = 'profile/address.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('address-list')


class AddressView(View):
    def post(self, request):
        pk = request.POST.get('id')
        address = {
            'address': request.POST.get('address'),
            'entrance_hall': request.POST.get('entrance_hall'),
            'floor': request.POST.get('floor'),
            'room': request.POST.get('room'),
            'description': request.POST.get('description'),
        }
        Address.objects.filter(pk=pk).update(**address)
        return redirect('address-list')


# ================================================wishlist================================

class WishlistListView(ListView):
    template_name = 'profile/wishlist.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).select_related('product')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wishlist_products = Wishlist.objects.filter(user=self.request.user).values_list('product_id', flat=True)
        context['wishlist_products'] = list(wishlist_products)
        return context

# ================================================notifications================================
class NotificationListView(ListView):
    queryset = Notification.objects.all()
    template_name = 'profile/notification.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')


# ================================================about-us================================
class AboutTemplateView(TemplateView):
    template_name = 'profile/about.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['settings'] = Settings.objects.first()
        return data

