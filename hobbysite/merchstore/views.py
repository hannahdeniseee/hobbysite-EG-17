from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Product


class MerchListView(ListView):
    model = Product
    template_name = 'merch_list.html'
    context_object_name = "products"


class MerchDetailView(DetailView):
    model = Product
    template_name = 'merch_detail.html'
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_type"] = self.object.product_type
        return context
