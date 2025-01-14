from django.shortcuts import render
from django.views.generic import ListView
from django.views import View

class ProductListView(ListView):
    ...

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

