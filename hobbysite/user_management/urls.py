"""
URL configuration for the user_management app.

Maps URL patterns to class-based views.
Includes routes for the dashboard and the profile update view.
"""

from django.urls import path
from .views import DashboardView
from .views import ProfileUpdateView

app_name = "user_management"

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('profile/<str:username>', ProfileUpdateView.as_view(),
         name='profile-update')
]
