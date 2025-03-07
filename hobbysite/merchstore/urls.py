from django.urls import path
from .views import MerchListView, MerchDetailView

urlpatterns = [
    path('items', MerchListView.as_view(), name="merch-list"),
    path('item/<int:pk>', MerchDetailView.as_view(), name='merch-detail')
]
# This might be needed, depending on your Django version
app_name = "merchstore"
