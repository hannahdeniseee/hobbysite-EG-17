from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from .models import Article, ArticleCategory
from .forms import ArticleForm


class ArticleListView(ListView):
    model = Article
    template_name = 'wiki/articles.html'
    context_object_name = 'articles'
    extra_context = {
        "articlecategories": ArticleCategory.objects.all()
    }


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'wiki/article.html'


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = "article_add.html"
    form_class = ArticleForm
    
    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)