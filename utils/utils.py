def total_cart_qty(cart):
    if isinstance(cart, dict):
        return sum([item['quantity'] for item in cart.values()])
    return 0

def total_cart_price(cart):
    sum_ = 0
    for item in cart.values():
        if item['quantitative_discount_price'] > 0:
            sum_ += item['quantitative_discount_price']
        else:
            sum_ += item['quantitative_price']
    return sum_

def total_order_price(order):
    sum_ = 0
    for item in order.items.all():
        if item.price_promotional > 0:
            sum_ += item.price_promotional
        else:
            sum_ += item.price
    return sum_