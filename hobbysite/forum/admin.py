from django.contrib import admin
from .models import Post, PostCategory


class PostInline(admin.TabularInline):
    model = Post


class PostCategoryAdmin(admin.ModelAdmin):
    model = PostCategory
    list_display = ('name', 'description')
    inlines = [PostInline, ]


class PostAdmin(admin.ModelAdmin):
    model = Post
    search_fields = ('title', 'category')
    list_display = ('title', 'category', 'created_on', 'updated_on')
    list_filter = ('category', 'created_on', 'updated_on')


admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Post, PostAdmin)
