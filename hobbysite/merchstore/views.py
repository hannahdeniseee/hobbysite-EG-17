from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Product, ProductType

class MerchListView(ListView):
    model = Product
    template_name = 'merch_list.html' 
    context_object_name = "products"

class MerchDetailView(DetailView):
    model = Product
    template_name = 'merch_detail.html' 