from forum.models import Thread
from django.views.generic.list import ListView
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .models import Profile
from .forms import ProfileUpdateForm
from merchstore.models import Product, Transaction
from blog.models import Article


class DashboardView(LoginRequiredMixin, ListView):
    model = Thread
    template_name = 'user_management/dashboard.html'
    context_object_name = 'threads'

    def get_queryset(self):
        return Thread.objects.filter(author=self.request.user.profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products_sold'] = Product.objects.filter(
            owner=self.request.user.profile)
        context['products_bought'] = Transaction.objects.filter(
            buyer=self.request.user.profile).distinct()
        context['blog_articles'] = Article.objects.filter(
            author=self.request.user.profile)
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'user_management/profile_form.html'
    form_class = ProfileUpdateForm

    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
        return reverse(
            'homepage',
        )
