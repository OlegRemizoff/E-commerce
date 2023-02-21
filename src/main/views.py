from django.shortcuts import render
from django.views.generic import DetailView
from django.http import HttpResponse
from .models import SmartPhone, Notebook




def index(requets):
    return HttpResponse("<h1>Django</h1>")


class ProductDetailView(DetailView):

    CT_MODEL_MODEL_CLASS = {
        "notebook": Notebook,
        "smartphone": SmartPhone, 
    }


    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    # model = Model
    # queryset = Models.objects.all()
    context_object_name = "product"
    template_name = 'main/product_detail.html'
    slug_url_kwarg = 'slug'