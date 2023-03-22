from django.db import models
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View
from .models import Category, Customer, Cart


# class CategoryDetailMixin(SingleObjectMixin):

#     def get_context_data(self, **kwargs: any) -> dict[str, any]:

#         context = super().get_context_data(**kwargs)
#         context['categories'] = Category.objects.get_category_for_navbar()
#         return context


class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):
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

        self.cart = cart
        return super().dispatch(request, *args, **kwargs)
    

def recalc_cart(cart):
    cart_data=cart.products.aggregate(models.Sum('final_price'), models.Count('id'))
    if cart_data.get('final_price__sum'):
        cart.final_price = cart_data['final_price__sum']
    else:
        cart.final_price = 0
    cart.total_products = cart_data['id__count'] 




# Olde cart_calculate
# def save(self, *args, **kwargs):
#     #sql функции интерпретированные Django
#     cart_data=self.products.aggregate(models.Sum('final_price'), models.Count('id'))
#     print(cart_data) #{'final_price__sum': None, 'id__count': 0}
#     if cart_data.get('final_price__sum'):
#         self.final_price = cart_data['final_price__sum']
#     else:
#         self.final_price = 0
#     self.total_products = cart_data['id__count'] 
#     return super().save(*args, **kwargs)