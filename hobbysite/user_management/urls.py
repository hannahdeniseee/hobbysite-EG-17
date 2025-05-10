from django.urls import path
from .views import DashboardView

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name='dashboard')
]

app_name = "user_management"
from django.urls import path
from .views import ProfileUpdateView

app_name = 'user_management'

urlpatterns = [
    path('profile/<str:username>/', ProfileUpdateView.as_view(), 
         name='profile-update'),
]
