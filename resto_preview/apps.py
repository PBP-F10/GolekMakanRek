from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.core.management import call_command

class RestoPreviewConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'resto_preview'

    def ready(self):
        post_migrate.connect(load_initial_data, sender=self)

def load_initial_data(sender, **kwargs):
    from .models import Restaurant
    try:
        if not Restaurant.objects.exists():
            print("Loading initial data from data.json...")
            call_command('loaddata', 'data.json')
    except Exception as e:
        print(f"Error loading initial data: {e}")


