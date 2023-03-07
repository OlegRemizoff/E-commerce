from django.shortcuts import render
from django.views.generic import DetailView, View
from .models import SmartPhone, Notebook, LatestProducts, Category


# def index(request):
#     products = LatestProducts.objects.get_products_for_main_page(
#         "smartphone", "notebook")
#     return render(request, 'main/index.html', {"products": products})


class HomeView(View):

    def get(self, request, *args, **kwargs):
        products = LatestProducts.objects.get_products_for_main_page(
            "smartphone", "notebook")
        return render(request, 'main/index.html', {"products": products})


class ProductDetailView(DetailView):

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


class CategoryDetailView(DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = "category"
    slug_url_kwarg = 'slug'
