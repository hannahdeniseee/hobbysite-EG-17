"""
This is the admin file to specify how the django admin is laid out with the
Commission app's models.
"""

from django.contrib import admin
from .models import Commission, Job, JobApplication


class JobInline(admin.TabularInline):
    """
    Creates the job inline for the commission admin.
    """
    model = Job


class JobAdmin(admin.ModelAdmin):
    """
    Creates the job admin panel.
    """
    model = Job


class JobApplicationAdmin(admin.ModelAdmin):
    """
    Creates the jobapplication admin panel.
    """
    model = JobApplication


class CommissionAdmin(admin.ModelAdmin):
    """
    Creates the commission admin panel and specifies search fields,
    list display, and list filter. Uses job inline.
    """
    model = Commission
    search_fields = ('title',)
    list_display = ('title', 'description', 'created_on', 'updated_on')
    list_filter = ('created_on', 'updated_on')
    inlines = [JobInline,]


admin.site.register(Job, JobAdmin,)
admin.site.register(Commission, CommissionAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
