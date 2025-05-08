"""
Django views for handling article-related pages.
"""

from django.shortcuts import render
from .models import Article, ArticleCategory
from django.views.generic import ListView, DetailView


class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'articles'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ArticleCategory.objects.all()
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'
