from django.shortcuts import redirect, render,reverse,get_object_or_404
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
        variation_id = self.request.GET.get('vid')
        is_simple_product = self.request.GET.get('is_simple_product') == 'true'

        if not variation_id:
            messages.error(self.request, 'Product not found')
            return redirect(http_referer)

        if is_simple_product:
            variation = get_object_or_404(models.Product, id=variation_id)
            product = variation
        else:
            variation = get_object_or_404(models.ProductVariation, id=variation_id)
            product = variation.product

        if variation.stock < 1:
            messages.error(self.request, 'Product out of stock')
            return redirect(http_referer)

        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session['cart']
        
        if variation_id in cart:
            cart_quantity = cart[variation_id]['quantity']
            cart_quantity += 1

            if variation.stock < cart_quantity:
                messages.warning(
                    self.request, 
                    f'Insufficient stock for {cart_quantity}x in {product.name}.'
                    f'Added {variation.stock}x to cart'
                )
                cart_quantity = variation.stock

            cart[variation_id]['quantity'] = cart_quantity
            cart[variation_id]['quantitative_price'] = cart[variation_id]['price'] * cart_quantity
            cart[variation_id]['quantitative_discount_price'] = cart[variation_id]['discount_price'] * cart_quantity
        else:
            cart[variation_id] = {
                'product_id': product.id,
                'name': product.name,
                'variation_name': variation.toStringAttributes() if not is_simple_product else '',
                'variation_id': variation.id if not is_simple_product else None,
                'price': variation.price,
                'discount_price': variation.discount_price,
                'quantitative_price': variation.price,
                'quantitative_discount_price': variation.discount_price,
                'quantity': 1,
                'slug': product.slug,
                'image': product.image.url,
            }
        self.request.session.save()
        messages.success(
            self.request,
            f'Product {product.name} {variation.toStringAttributes() if not is_simple_product else '' } '
            f'added to cart ({cart[variation_id]["quantity"]}x)'
            )
        return redirect(http_referer)

class RemoveFromCartView(View):
    ...

class CartView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'product/cart.html')

class FinalizeView(View):
    ...

