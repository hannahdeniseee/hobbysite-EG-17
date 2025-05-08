from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('accounts:login') 

    def form_valid(self, form):
        messages.success(self.request, 'Account created successfully!')
        return super().form_valid(form)
   

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


class CustomLogoutView(LogoutView):
    next_page = '/'  # Redirect to home or another page after logout


class ProfileDetailView(DetailView):
    model = User
    template_name = 'registration/profile.html'
    context_object_name = 'user'

    def get_object(self):
        # Return the current logged-in user’s profile
        return self.request.user


class ProfileUpdateView(UpdateView):
    model = User
    fields = ['username', 'email']  # You can add more fields as needed
    template_name = 'registration/profile_update.html'
    success_url = reverse_lazy('accounts:profile')  # Redirect to profile view after update

    def get_object(self):
        return self.request.user