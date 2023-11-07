from django.apps import AppConfig


class AlarmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.alarms'

    def ready(self):
        from . import signals