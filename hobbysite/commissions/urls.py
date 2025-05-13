from django.urls import path
from .views import CommissionListView, CommissionDetailView, CommissionCreateView, CommissionUpdateView


urlpatterns = [
     path('list', 
         CommissionListView.as_view(), name='commissions-list'),
     path('detail/<int:pk>', 
         CommissionDetailView.as_view(), name='commission-detail'),
     path('create',
          CommissionCreateView.as_view(), name='commission-create')
]


app_name = 'commissions'
