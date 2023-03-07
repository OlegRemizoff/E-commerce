from django.urls import path, include
from .views import HomeView, ProductDetailView, CategoryDetailView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('products/<str:ct_model>/<str:slug>/',
         ProductDetailView.as_view(), name="product_detail"),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail')
]
