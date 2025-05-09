from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from user_management.models import Profile


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('accounts:login') 

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object, 
                               display_name=self.object.username)
        return response
   

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


class CustomLogoutView(LogoutView):
    next_page = '/' 


class ProfileDetailView(DetailView):
    model = User
    template_name = 'registration/profile.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user


class ProfileUpdateView(UpdateView):
    model = User
    fields = ['username', 'email']  
    template_name = 'registration/profile_update.html'
    success_url = reverse_lazy('accounts:profile') 

    def get_object(self):
        return self.request.user