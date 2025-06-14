from django.contrib import admin
from .models import Article, ArticleCategory, Comment


class ArticleInline(admin.TabularInline):
    model = Article


class ArticleCategoryAdmin(admin.ModelAdmin):
    model = ArticleCategory
    list_display = ('name', 'description')
    inlines = [ArticleInline]


class ArticleAdmin(admin.ModelAdmin):
    model = Article
    search_fields = ('title', 'category')
    list_display = ('title', 'category', 'created_on', 'updated_on')
    list_filter = ('category', 'created_on', 'updated_on')


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('author', 'article', 'entry')


admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Article, ArticleAdmin)
