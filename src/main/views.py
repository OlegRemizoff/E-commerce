from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, View

from .models import SmartPhone, Notebook, LatestProducts
from .models import Category, CartProduct
from .utils import CartMixin

# def index(request):
#     products = LatestProducts.objects.get_products_for_main_page(
#         "smartphone", "notebook")
#     return render(request, 'main/index.html', {"products": products})


# class HomeView(TemplateView):
#     template_name = 'main/index.html'


#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         products = LatestProducts.objects.get_products_for_main_page(
#         "smartphone", "notebook")
#         context['products'] = products
#         return context

class HomeView(View):

    def get(self, request, *args, **kwargs):
        products = LatestProducts.objects.get_products_for_main_page(
            "smartphone", "notebook")
        return render(request, 'main/index.html', {"products": products})


class ProductDetailView(CartMixin, DetailView):

    CT_MODEL_MODEL_CLASS = {
        "notebook": Notebook,
        "smartphone": SmartPhone,
    }

    def dispatch(self, request, *args, **kwargs):
        # забираем имя модели из **kwargs (urls/path(<str:ct_model>) ) и оределяем имя модели
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    # model = Model
    # queryset = Models.objects.all()
    context_object_name = "product"
    template_name = 'main/product_detail.html'
    slug_url_kwarg = 'slug'

    # получение __str__ о конкретной модели
    # для добавления товара в корзину с помощью этой вьюхи
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        return context


class CategoryDetailView(DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = "category"
    slug_url_kwarg = 'slug'


class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        # Забираем нужные значения из словаря
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        # Через content_type = определяем модель нашего товара
        content_type = ContentType.objects.get(model=ct_model)
        # Обращаемся к родительскому классу и через  менеджер находим продукт
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        if created:
            self.cart.products.add(cart_product)
        self.cart.save()
        # print(ct_model, product_slug)
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(CartMixin, View):

    def get(self,request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product= CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        self.cart.save()
        return HttpResponseRedirect('/cart/')


class CartChangeQTYView(CartMixin, View):

    def post(self,request, *args, **kwargs):
        # print(request.POST)
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product= CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        qty = int(request.POST.get('qty'))
        cart_product.qty = qty
        cart_product.save()
        self.cart.save() # для обновления информации в корзине
        return HttpResponseRedirect('/cart/')



class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        # customer = Customer.objects.get(user=request.user) CartMixin
        # cart = Cart.objects.get(owner=customer)
        # categories = Category.objects.get_category_for_navbar()

        return render(request, 'main/cart.html', {'cart': self.cart})
