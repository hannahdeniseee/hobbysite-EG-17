from django.contrib import admin
from .models import Article

class RecipeAdmin(admin.ModelAdmin):
    model = Article

admin.site.register(Article, RecipeAdmin)
