from .models import Cart

def cart_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        user_cart = Cart.objects.get_or_create(user=request.user)[0]
        cart_count = user_cart.cart_items.count()
    return {'cart_count': cart_count}