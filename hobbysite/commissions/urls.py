"""
URL configuration for the Commissions app.

Maps URL patterns to class-based views.
Includes routes for commissions list, commission detail view,
and creating and updating the commissions.
"""

from django.urls import path
from .views import (CommissionListView, CommissionDetailView,
                    CommissionCreateView, CommissionUpdateView)


urlpatterns = [
     path('list', CommissionListView.as_view(), name='commissions-list'),
     path('detail/<int:pk>', CommissionDetailView.as_view(),
          name='commission-detail'),
     path('add', CommissionCreateView.as_view(), name='commission-add'),
     path('<int:pk>/edit', CommissionUpdateView.as_view(),
          name='commission-edit')
]


app_name = 'commissions'
