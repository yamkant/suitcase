from django.apps import AppConfig


class AlarmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'alarms'

    def ready(self):
        from . import signals