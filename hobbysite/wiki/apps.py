from django.apps import AppConfig
from django.core.files.storage import default_storage
from django.conf import settings
from importlib import import_module


class WikiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wiki'
    
    def ready(self):
        if hasattr(settings, 'DEFAULT_FILE_STORAGE'):
            module_path, class_name = settings.DEFAULT_FILE_STORAGE.rsplit('.', 1)
            storage_module = import_module(module_path)
            storage_class = getattr(storage_module, class_name)
            # Force Django to use your MediaStorage as the default
            from django.core.files import storage as storage_module
            storage_module.default_storage = storage_class()