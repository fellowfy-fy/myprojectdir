from .models import Order

def orders(request):
    """
    A function that takes a request and returns a dictionary of categories.
    """
    if request.user.is_authenticated:
        orders = Order.objects.filter(user = request.user)
    else:
        orders = []
    return {'orders': orders}

def all_orders(request):
    """
    A function that takes a request and returns a dictionary of categories.
    """
    orders = Order.objects.filter()
    return {'orders': orders}