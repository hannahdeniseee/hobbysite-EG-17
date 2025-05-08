from django.urls import path
from .views import ProfileUpdateView

app_name = 'user_management'

urlpatterns = [
    path('profile/<str:username>/', ProfileUpdateView.as_view(), 
         name='profile-update'),
]
