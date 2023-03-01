from django.shortcuts import render
from django.views.generic import DetailView
from .models import SmartPhone, Notebook, LatestProducts, Category


def index(request):
    categories = Category.objects.get_category_for_navbar()
    products = LatestProducts.objects.get_products_for_main_page(
        "smartphone", "notebook")
    return render(request, 'main/index.html', {"products": products, 'categories': categories})


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
