from django.shortcuts import render
from .models import Article

def article_list(request):
    """
    View function for displaying a list of recipes.
    """
    articles = Article.objects.all()

    ctx = {
        'articles': articles
    }
    return render(request, 'article_list.html', ctx)

def article_detail(request, id):
    """
    View function for displaying the details of a recipe.
    """
    ctx = { 
        'article': Article.objects.get(id=id) 
    }
    return render(request, 'article_detail.html', ctx)