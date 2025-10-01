from django.shortcuts import render
from django.views.generic import ListView, View
from django.utils.translation import get_language
from apps.models import Products, Category


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




class ProductSearchView(View):
    def post(self, request):
        query = request.POST.get('name', '')
        lang = get_language()

        # Parlerda tarjimalar `translations__fieldname` orqali olinadi
        products = Products.objects.filter(
            translateions__language_code=lang,
            translateions__name__icontains=query
        )

        return render(request, 'search/search.html', {'products': products})

