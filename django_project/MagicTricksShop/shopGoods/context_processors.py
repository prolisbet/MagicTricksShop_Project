def cart_item_count(request):
    cart = request.session.get('cart', {})
    total_items = sum(cart.values())
    return {'total_items': total_items}
