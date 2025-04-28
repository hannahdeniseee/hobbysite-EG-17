from django.contrib import admin

from .models import Commission, Comment


class CommentInline(admin.TabularInline):
    model = Comment


class CommentAdmin(admin.ModelAdmin):
    model = Comment


class CommissionAdmin(admin.ModelAdmin):
    model = Commission
    search_fields = ('title',)
    list_display = ('title', 'description', 'created_on', 'updated_on')
    list_filter = ('created_on', 'updated_on')
    inlines = [CommentInline,]


admin.site.register(Comment, CommentAdmin)
admin.site.register(Commission, CommissionAdmin)
