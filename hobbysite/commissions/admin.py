from django.contrib import admin

from .models import Commission, Job


class JobInline(admin.TabularInline):
    model = Job


class JobAdmin(admin.ModelAdmin):
    model = Job


class CommissionAdmin(admin.ModelAdmin):
    model = Commission
    search_fields = ('title',)
    list_display = ('title', 'description', 'created_on', 'updated_on')
    list_filter = ('created_on', 'updated_on')
    inlines = [JobInline,]


admin.site.register(Job, JobAdmin)
admin.site.register(Commission, CommissionAdmin)
