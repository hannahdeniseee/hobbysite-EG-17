"""
Django views for handling article-related pages.
"""

from django.shortcuts import render
from .models import Article, ArticleCategory

def article_list(request):
    """
    View function for displaying the list view of blog.
    """
    articles = Article.objects.all()
    categories = ArticleCategory.objects.all()

    ctx = {
        'articles': articles,
        'categories': categories,
    }
    return render(request, 'article_list.html', ctx)

def article_detail(request, id):
    """
    View function for displaying the detail view of each article.
    """
    ctx = {
        'article': Article.objects.get(id=id) 
    }
    return render(request, 'article_detail.html', ctx)
