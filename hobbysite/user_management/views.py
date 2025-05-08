from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Profile


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'user_management/profile_form.html'

    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy('user_management:profile-update', 
                            kwargs={'username': self.request.user.username})
