from django.contrib import admin
from .models import Post, PostCategory


class TaskInline(admin.TabularInline):
    model = Post


class TaskGroupAdmin(admin.ModelAdmin):
    model = PostCategory
    inlines = [TaskInline, ]


class TaskAdmin(admin.ModelAdmin):
    model = Post
    search_fields = ('title', 'category')
    list_display = ('title', 'category', 'created_on', 'updated_on')
    list_filter = ('category', 'created_on', 'updated_on')


admin.site.register(PostCategory, TaskGroupAdmin)
admin.site.register(Post, TaskAdmin)
