from django.urls import path
from .views import DashboardView
from .views import ProfileUpdateView

app_name = "user_management"

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('profile/<str:username>', ProfileUpdateView.as_view(),
         name='profile-update')
]
