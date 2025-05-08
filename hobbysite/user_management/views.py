from forum.models import Thread
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, ListView):
    model = Thread
    template_name = 'user_management/dashboard.html'
    context_object_name = 'threads'

    def get_queryset(self):
        return Thread.objects.filter(author=self.request.user.profile)
