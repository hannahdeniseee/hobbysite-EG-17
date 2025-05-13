from django.urls import path
from .views import ProductListView, ProductDetailView
from .views import ProductCreateView, ProductUpdateView, CartView
from .views import TransactionListView

urlpatterns = [
    path('items', ProductListView.as_view(), name="merch-list"),
    path('item/<int:pk>', ProductDetailView.as_view(), name='merch-detail'),
    path('item/add', ProductCreateView.as_view(), name='merch-add'),
    path('item/<int:pk>/edit', ProductUpdateView.as_view(), name='merch-edit'),
    path('cart', CartView.as_view(), name='merch-cart'),
    path('transactions', TransactionListView.as_view(), name='transactions'),
]

app_name = "merchstore"
