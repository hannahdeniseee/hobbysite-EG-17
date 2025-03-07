from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Article, ArticleCategory


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
