from django.urls import path
from .views import HomeView, ProductDetailView, CategoryDetailView, CartView,AddToCartView, DeleteFromCartView, CartChangeQTYView, CheckoutView, MakeOrderView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('products/<str:ct_model>/<str:slug>/',
         ProductDetailView.as_view(), name="product_detail"),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:ct_model>/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<str:ct_model>/<str:slug>/', DeleteFromCartView.as_view(), name='remove_from_cart'),    
    path('change-qty/<str:ct_model>/<str:slug>/', CartChangeQTYView.as_view(), name='change_qty'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('make-order/', MakeOrderView.as_view(), name='make_order'),

]
