from django.template.context_processors import request
from main.models import Customer, Cart



def get_cart_quantity(request):
    customer = Customer.objects.get(user=request.user)
    cart = Cart.objects.get(owner=customer)
    return {'cart': cart}