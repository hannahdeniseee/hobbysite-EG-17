from django.apps import AppConfig


class WikiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wiki'
    
    def ready(self):
        from django.conf import settings
        settings.DEFAULT_FILE_STORAGE = 'hobbysite.storage_backends.MediaStorage'