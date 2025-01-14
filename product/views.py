from django.shortcuts import render
from django.views.generic import ListView,DetailView
from django.views import View
from . import models

class ProductListView(ListView):
    model = models.Product
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 10

class ProductDetailView(DetailView):
    model = models.Product
    template_name = 'product/detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'


class AddToCartView(View):
    ...

class RemoveFromCartView(View):
    ...

class CartView(View):
    ...

class FinalizeView(View):
    ...

