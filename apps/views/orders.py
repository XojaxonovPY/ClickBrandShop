from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, View

from apps.forms import OrderItemModelForm
from apps.models import OrderItem, Order, Payment, Address


class OrderItemCreateView(CreateView):
    form_class = OrderItemModelForm
    template_name = 'market/detail.html'
    success_url = reverse_lazy('main')


class OderItemListView(ListView):
    queryset = OrderItem.objects.all()
    template_name = 'orders/orders_item.html'
    context_object_name = 'items'

    def get_queryset(self):
        query = super().get_queryset()
        return query.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = context['items']
        context['total_price'] = sum(item.total_price for item in items)
        return context


class OrderItemDeleteView(DeleteView):
    queryset = OrderItem.objects.all()
    template_name = 'orders/orders_item.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('item-list')


class OrderItemView(View):
    def post(self, request, pk):
        item = OrderItem.objects.get(pk=pk)
        action = request.POST.get('action')
        if action == 'plus':
            item.quantity += 1
        elif action == 'minus' and item.quantity > 1:
            item.quantity -= 1
        item.save()
        return redirect('item-list')


class OrderListView(ListView):
    queryset = OrderItem.objects.all()
    template_name = 'orders/order.html'
    context_object_name = 'orders'

    def get_queryset(self):
        query = super().get_queryset()
        return query.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        items = context['orders']
        context['total_price'] = sum(item.total_price for item in items)
        context['delivery'] = Order.OrderType.DELIVERY.value
        context['take_away'] = Order.OrderType.TAKE_AWAY.value
        return context


class OrderCreateView(View):
    def post(self, request):
        address={
            'address':request.POST.get('address'),
            'entrance_hall':request.POST.get('entrance_hall'),
            'floor':request.POST.get('floor'),
            'room':request.POST.get('room'),
            'description':request.POST.get('description'),
            'user':request.user,
        }
        Address.objects.create(**address)
        payment={
            'payment_method': request.POST.get('payment_method'),
            'user':request.user,
            'total_price':request.POST.get('total_price')
        }
        Payment.objects.create(**payment)
        delivery_type = request.POST.get('type')
        items = request.POST.getlist('items[]')
        prices = request.POST.getlist('total_price[]')
        for item_id, price in zip(items, prices):
            Order.objects.create(
                total_price=float(price),
                item_id=int(item_id),
                type=delivery_type,
            )

        return redirect('main')




