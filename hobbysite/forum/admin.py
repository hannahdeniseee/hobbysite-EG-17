from django.contrib import admin
from .models import Thread, Comment, ThreadCategory


class ThreadInline(admin.TabularInline):
    model = Thread


class CommentInline(admin.TabularInline):
    model = Comment


class ThreadCategoryAdmin(admin.ModelAdmin):
    model = ThreadCategory
    list_display = ('name', 'description',)
    inlines = [ThreadInline,]


class ThreadAdmin(admin.ModelAdmin):
    model = Thread
    search_fields = ('title', )
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


admin.site.register(ThreadCategory, ThreadCategoryAdmin)
admin.site.register(Thread, ThreadAdmin)
