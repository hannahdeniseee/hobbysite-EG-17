"""
Django views for handling article-related pages.
"""

from django.shortcuts import render
from .models import Article, ArticleCategory
from django.views.generic import ListView, DetailView


class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'blog'
    context = {
        'categories': ArticleCategory.objects.all()
    }

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'
