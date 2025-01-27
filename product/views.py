from django.shortcuts import redirect, render,reverse,get_object_or_404
from django.views.generic import ListView,DetailView
from django.views import View
from django.contrib import messages
from . import models
from user_profile.models import UserProfile
from django.db.models import Q

class ProductListView(ListView):
    model = models.Product
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 10
    ordering = ['-id']

class SeachProductView(ProductListView):
    def get_queryset(self, *args, **kwargs):
        term = self.request.GET.get('term') or self.request.session['term']
        qs = super().get_queryset(*args, **kwargs)

        if not term:
            return qs

        self.request.session['term'] = term

        qs = qs.filter(
            Q(name__icontains=term) |
            Q(long_description__icontains=term) |
            Q(short_description__icontains=term)
        )

        self.request.session.save()

        return qs
    
class ProductDetailView(DetailView):
    model = models.Product
    template_name = 'product/detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

class AddToCartView(View):
    def get(self,*args, **kwargs):
        # if self.request.session.get('cart'):
        #     del self.request.session['cart']
        #     self.request.session.save()

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
            item_id = str(product.id)
        else:
            variation = get_object_or_404(models.ProductVariation, id=variation_id)
            product = variation.product
            item_id = str(variation.id) + 'v'

        if variation.stock < 1:
            messages.error(self.request, 'Product out of stock')
            return redirect(http_referer)

        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session.get('cart')

        if item_id in cart:
            cart_quantity = cart[item_id]['quantity']
            cart_quantity += 1

            if variation.stock < cart_quantity:
                messages.warning(
                    self.request, 
                    f'Insufficient stock for {cart_quantity}x in {product.name}.'
                    f'Added {variation.stock}x to cart'
                )
                cart_quantity = variation.stock

            cart[item_id]['quantity'] = cart_quantity
            cart[item_id]['quantitative_price'] = cart[item_id]['price'] * cart_quantity
            cart[item_id]['quantitative_discount_price'] = cart[item_id]['discount_price'] * cart_quantity
        else:
            cart[item_id] = {
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
            f'Product {cart[item_id]["name"]} {cart[item_id]["variation_name"] + ' ' if cart[item_id]["variation_name"] else ''}'
            f'added to cart ({cart[item_id]["quantity"]}x)'
            )
        return redirect(http_referer)

class RemoveFromCartView(View):
    def get(self,*args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('product:list')
            )
        variation_id = self.request.GET.get('vid')
        if not variation_id:
            messages.error(self.request, 'Product not found')
            return redirect(http_referer)

        cart = self.request.session.get('cart', {})
        if variation_id in cart:
            product = cart[variation_id]
            messages.success(
                self.request,
        f'Product {product['name']} {product['variation_name'] + ' ' if product['variation_name'] else ''} '
        'removed from cart'
        )
            del cart[variation_id]
            self.request.session.save()
        else:
            messages.error(self.request, 'Product not found in cart')
        return redirect(http_referer)

class CartView(View):
    def get(self, *args, **kwargs):
        context = {
            'cart': self.request.session.get('cart', {}),
        }
        return render(self.request, 'product/cart.html',context)

class ResumeView(View):
    def get(self,*args, **kwargs):

        if not self.request.user.is_authenticated:
            messages.error(self.request, 'You must be logged in to proceed to checkout')
            return redirect(reverse('profile:create'))

        profile = UserProfile.objects.filter(user=self.request.user).exists()
        if not profile:
            messages.error(self.request, 'You must have a profile to proceed to checkout')
            return redirect(reverse('profile:create'))

        if not self.request.session.get('cart'):
            messages.error(self.request, 'Your cart is empty')
            return redirect(reverse('product:list'))

        context = {
            'user': self.request.user,
            'cart': self.request.session.get('cart', {}),
        }

        return render(self.request, 'product/resume.html', context)

