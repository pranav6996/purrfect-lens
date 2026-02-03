import os
from django.apps import AppConfig


class CatsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cats"

    def ready(self):
        # We import here to avoid RegistryNotReady issues
        if os.environ.get('RUN_MAIN') or os.environ.get('GUNICORN_CMD_ARGS'):
            from .ml_utils import load_model_and_labels
            print("Eagerly loading Keras model...")
            load_model_and_labels()
