from django.http import HttpResponse
from django.shortcuts import redirect,reverse
from django.views.generic import DetailView
from django.views import View
from django.contrib import messages
from product.models import Product, ProductVariation
from utils import utils
from .models import Order, OrderItem

class DispatchLoginRequired(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(self.request, "You need to login to continue")
            return redirect('profile:create')
        return super().dispatch(*args, **kwargs)

class PaymentView(DispatchLoginRequired,DetailView):
    template_name = 'order/payment.html'
    model = Order
    pk_url_kwarg = 'pk'
    context_object_name = 'order'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user=self.request.user)
        return qs


class SaveOrderView(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(self.request, "You need to login to continue")
            return redirect('profile:create')

        if not self.request.session.get('cart'):
            messages.error(self.request, "You need to add items to cart to continue")
            return redirect('product:list')

        cart = self.request.session.get('cart')
        msgs = []

        for product_id in cart:
            product_id = str(product_id)
            product = Product.objects.get(id=cart[product_id]['product_id'])
            variation = product

            if cart[product_id].get('variation_id'):
                variation = ProductVariation.objects.get(id=cart[product_id]['variation_id'])
                product = variation.product

            stock = variation.stock
            price = variation.price
            discount_price = variation.discount_price

            if stock < cart[product_id]['quantity']:
                cart[product_id]['quantity'] = stock
                cart[product_id]['quantitative_price'] = stock * price
                cart[product_id]['quantitative_discount_price'] = stock * discount_price

                msgs.append(f"Insufficient stock for {product.name}. Quantity has been adjusted to {stock}")

        if msgs:
            for msg in msgs:
                messages.error(self.request, msg)
            self.request.session.save()
            return redirect('product:cart')

        order = Order(
            user=self.request.user,
            total=utils.total_cart_price(cart),
            total_qty=utils.total_cart_qty(cart),
            status='C'
            )

        order.save()

        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    product_id=v['product_id'],
                    product=v['name'],
                    variation=v['variation_name'],
                    variation_id=v['variation_id'],
                    price=v['quantitative_price'],
                    price_promotional=v['quantitative_discount_price'],
                    quantity=v['quantity'],
                    image=v['image']
                )
                for v in cart.values()
            ]
        )

        del self.request.session['cart']

        return redirect(
            reverse('order:payment',
                    kwargs={'pk': order.id}
                    )
        )

class DetailOrderView(View):
    pass