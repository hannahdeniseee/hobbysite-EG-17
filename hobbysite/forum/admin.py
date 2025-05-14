"""
This is the admin file to specify how the django admin is laid out with the
Forum app's models.
"""

from django.contrib import admin
from .models import Thread, Comment, ThreadCategory


class ThreadInline(admin.TabularInline):
    """
    Creates the thread inline for the thread category admin.
    """
    model = Thread


class CommentInline(admin.TabularInline):
    """
    Creates the comment inline for the thread admin.
    """
    model = Comment


class ThreadCategoryAdmin(admin.ModelAdmin):
    """
    Specifies the displayed inlines and fields for the thread category admin.
    """
    model = ThreadCategory
    list_display = ('name', 'description',)
    inlines = [ThreadInline,]


class ThreadAdmin(admin.ModelAdmin):
    """
    Specifies the search fields, filters, and displayed inlines and fields
    for the thread admin.
    """
    model = Thread
    search_fields = ('title', 'author', 'category', )
    list_display = ('title',
                    'author',
                    'category',
                    'image',
                    'created_on',
                    'updated_on',
                    )
    list_filter = ('author',
                   'category',
                   'created_on',
                   'updated_on',
                   )
    inlines = [CommentInline,]


class CommentAdmin(admin.ModelAdmin):
    """
    Specifies the search fields, filters, and displayed fields
    for the comment admin.
    """
    model = Comment
    search_fields = ('author', 'thread', )
    list_display = ('author', 'thread', 'created_on', 'updated_on', )
    list_filter = ('author', 'thread', 'created_on', 'updated_on', )


admin.site.register(ThreadCategory, ThreadCategoryAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Comment, CommentAdmin)
