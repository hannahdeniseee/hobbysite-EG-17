'''
URL configuration for the blog app. 
'''

from django.urls import path
from .views import article_list, article_detail

urlpatterns = [
    path('articles', article_list, name="recipe_list"),
    path('article/<int:id>', article_detail, name="recipe_detail"),
]

app_name = "ledger"
