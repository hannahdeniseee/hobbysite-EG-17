from django.urls import path
from .views import RegisterView, CustomLoginView
from .views import ProfileDetailView, ProfileUpdateView, CustomLogoutView
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', ProfileDetailView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), 
         name='profile_update'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), 
         name='password_reset'),
]