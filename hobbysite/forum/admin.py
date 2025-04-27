from django.contrib import admin
from .models import Thread, ThreadCategory


class ThreadInline(admin.TabularInline):
    model = Thread


class ThreadCategoryAdmin(admin.ModelAdmin):
    model = ThreadCategory
    list_display = ('name', 'description')
    inlines = [ThreadInline, ]


class ThreadAdmin(admin.ModelAdmin):
    model = Thread
    search_fields = ('title', 'category')
    list_display = ('title', 'category', 'created_on', 'updated_on')
    list_filter = ('category', 'created_on', 'updated_on')


admin.site.register(ThreadCategory, ThreadCategoryAdmin)
admin.site.register(Thread, ThreadAdmin)
