from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from . import models

class ProductListView(ListView):
    model = models.Product
    template_name = 'product/list.html'
    context_object_name = 'products'


class ProductDetailView(View):
    ...

class AddToCartView(View):
    ...

class RemoveFromCartView(View):
    ...

class CartView(View):
    ...

class FinalizeView(View):
    ...

