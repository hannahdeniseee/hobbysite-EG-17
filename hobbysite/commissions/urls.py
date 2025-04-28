from django.urls import path
from .views import commissions_list, commissions_detail


urlpatterns = [
    path('list', 
         commissions_list, name='commissions-list'),
    path('detail/<int:pk>', 
         commissions_detail, name='commission-detail')
]


app_name = 'commissions'
