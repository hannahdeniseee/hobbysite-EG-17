from django.urls import path
from .views import commissions_list, commissions_detail


urlpatterns = [
    path('commissions/list/', commissions_list, name='commissions-list'),
    path('commissions/detail/<int:pk>/', commissions_detail, name='commission-detail')
]


app_name = 'commissions'