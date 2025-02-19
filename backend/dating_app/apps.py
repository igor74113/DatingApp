# this folder contains django apps configurations 
from django.apps import AppConfig


class DatingAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dating_app"

    # added by Jessica -- attempt to debug profile creation with signals.py
    def ready(self): 
        import dating_app.signals # ensures that signals.py is being imported
