from django.template.context_processors import request
from main.models import Customer, Cart



def get_cart_quantity(request):
    # customer = Customer.objects.get(user=request.user)
    # cart = Cart.objects.get(owner=customer)
    # return {'cart': cart}

    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        if not customer:
            customer = Customer.objects.create(user=request.user)
        cart = Cart.objects.filter(owner=customer, in_order=False).first()
        if not cart:
            cart = Cart.objects.create(owner=customer)
    else:
        cart = Cart.objects.filter(for_anonymous_user=True).first()
        if not cart:
            cart = Cart.objects.create(for_anonymous_user=True)
    return {'cart': cart}