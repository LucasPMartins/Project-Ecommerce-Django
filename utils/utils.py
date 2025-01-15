def total_cart_qty(cart):
    return sum([item['quantity'] for item in cart.values()])

def total_cart_price(cart):
    sum_ = 0
    for item in cart.values():
        if item['quantitative_discount_price'] > 0:
            sum_ += item['quantitative_discount_price']
        else:
            sum_ += item['quantitative_price']
    return sum_