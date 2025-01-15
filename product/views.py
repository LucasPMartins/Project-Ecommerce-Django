from django.http import HttpResponse
from django.shortcuts import redirect,reverse,get_object_or_404
from django.views.generic import ListView,DetailView
from django.views import View
from django.contrib import messages
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
    def get(self,*args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('product:list')
            )
        product_id = self.request.GET.get('vid')
        is_simple_product = self.request.GET.get('is_simple_product') == 'true'

        if not product_id:
            messages.error(self.request, 'Product not found')
            return redirect(http_referer)

        if is_simple_product:
            product = get_object_or_404(models.Product, id=product_id)
            variant = None
        else:
            variant = get_object_or_404(models.ProductVariation, id=product_id)
            product = variant.product

        print('Product:', product)
        print('Variant:', variant)

        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session['cart']
        
        if product_id in cart:
            # cart[variant_id] += 1
            pass
        else:
            pass

        return HttpResponse(f'Added to cart:{product.name} {variant.toStringAttributes() if variant else ""}')

class RemoveFromCartView(View):
    ...

class CartView(View):
    ...

class FinalizeView(View):
    ...

